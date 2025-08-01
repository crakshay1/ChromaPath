# coding: utf-8
import tkinter as tk
import geopandas as gpd
import matplotlib.pyplot as plt
import requests
import json
import os
import random
import EntitiesV2
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

print("Hey huzz")
## Interface graphique
fenetre = tk.Tk()
fenetre.title("Voyageur du commerce - Hugo X Akshay")

# Pays au choix
path = "Pays"
dir_list = os.listdir(path) # Tous les fichiers .shp sont dans le répertoire
liste_p = []
for element in dir_list:
    liste_p.append(element[:2]) # On rajoute les noms de fichiers dans notre liste
liste_pays = list(set(liste_p)) # Il y a des doublons dû à la présence de fichiers .shx et .shp
# ON BOYCOTT FORT
liste_pays.remove("il") 
liste_pays.remove("ru") 


def get_country(pais: str, n: int) -> list: # Oui "pais" c'est "pays" en espagnol (je crois)
    """
        Prend en compte un pays et renvoie
        les informations concernant ses villes
    """
    # Obtention des villes et de leurs informations
    user = "crakshay" # hugot_s
    api_url = 'http://api.geonames.org/searchJSON?country={}&featureClass=P&maxRows={}&username={}'.format(pais, n, user)
    response = requests.get(api_url, headers=None)
    cities = json.loads(response.text) 
    # Le résultat étant un str, utiliser le module le json nous permet de le transformer en dict
    if len(cities["geonames"]) > 0:
        return cities
    else:
        return -1

# Pour la sélection du pays
new_dico = {}
for element in liste_pays:
    pays = get_country(element,1)
    # Si on a les fichiers du pays et que l'API fournit des infos sur celui-ci
    if pays != -1:
        new_dico.update({pays["geonames"][0]["countryName"]:pays["geonames"][0]["countryCode"] })
    # Si l'API n'a aucune info sur le pays, on supprime les fichiers shp et shx
    if pays == -1:
        os.remove("Pays/"+element+".shp")
        os.remove("Pays/"+element+".shx")

select_frame = tk.Frame(fenetre)
select_frame.pack(pady=10)
liste = ttk.Combobox(select_frame, values=list(sorted(new_dico.keys()))) 
liste.current(0)

# Nombre de villes générées aléatoirement
nombre = tk.Label(select_frame, text="Choisir le nombre de villes à générer:", bg="#fa9cdb")
pays = tk.Label(select_frame, text="Choisir le pays à générer:", bg="#fa9cdb")
scroll = tk.Spinbox(select_frame, from_=0, to=1000)

# Indications
tutorial_frame = tk.Frame(fenetre)
tutorial_frame.pack(pady=30)
cam = tk.Label(tutorial_frame, text="←↓↑→: Déplacer la caméra", bg="#fa9cdb")
zooming = tk.Label(tutorial_frame, text = "A: Dezoomer     |     E: Zoomer", bg="#fa9cdb")

def generer_carte():
    """
        Prend en compte le nombre N de villes générées aléatoirement, et le pays retenu
        Et génère la carte avec les villes
    """
    # On obtient les informations retenues dans la fenêtre
    N = int(scroll.get())
    country = new_dico[liste.get()].lower()
    pays = "Pays/"+country+".shp" 

    # On crée la carte
    carte = gpd.read_file(pays)
    carte.plot(ax=ax, color="#fa9cdb", edgecolor="black")

    # Liste des villes aléatoirement générées
    villes = get_country(country, 1000)
    choix_random = [] 
    choix_random.append(random.sample(villes["geonames"], min(N,len(villes["geonames"]))))
    # Même si on dépasse le nombre de villes voulu avec N, on prendra le nombre max de villes du pays

    # On crée les villes comme des objets
    global liste_v, nom_vers_ville
    liste_v = []
    for ville in choix_random[0]:
        liste_v.append(EntitiesV2.Ville(ville['name'], float(ville['lng']), float(ville['lat'])))
    
    # On place les villes sur la carte
    liste_n = []
    for v in liste_v:
        ax.scatter(v.lng, v.lat, color="black", marker="o", zorder=5)
        ax.text(v.lng, v.lat, v.name, fontsize=8, ha="right", color="#6A0DAD")
        liste_n.append(v.name)
    nom_vers_ville = {v.name: v for v in liste_v}

    # Sélection de la ville de départ 
    global depart, listeVilles
    depart = tk.Label(select_frame, text="Choisir la ville de départ", bg="#fa9cdb")
    depart.grid(row=0, column=2, padx=10)
    listeVilles = ttk.Combobox(select_frame, values=liste_n)
    listeVilles.current(0)
    listeVilles.grid(row=1, column=2, padx=10)

    # Sélection nombre générations
    global gen, select_gen
    select_gen = tk.Label(select_frame, text="Choisir le nombre de générations", bg="#fa9cdb")
    select_gen.grid(row=0, column=3, padx=10)
    gen = tk.Spinbox(select_frame, from_=1, to=10000)
    gen.grid(row = 1, column=3, padx=10)
    

def algo():
    """
        Execute notre algorithme de parcours
    """
    depart_v = listeVilles.get()
    nb_gen = int(gen.get())
    start = nom_vers_ville[depart_v]

    # Création population
    liste_c = []
    for i in range(200): # Taille de la population
        route = EntitiesV2.Route(start,liste_v)
        route.trace_ma_route()
        liste_c.append(route)
    populasse = EntitiesV2.Population(liste_c, start, liste_v)

    # Sélection tah la Champion's league
    fenetre2 = tk.Toplevel(fenetre)
    fenetre2.title("Voyageur du commerce - Resultats")
    resultats = tk.Text(fenetre2, width=50, height=25, bg="#fa9cdb")
    resultats.pack()

    best_dist = float('inf')
    best_chemin = None
    for generation in range(nb_gen):
        populasse.generer_nouvelle_population()
        meilleure_route = populasse.election()
        meilleure_route.get_villes()
        if meilleure_route.distance < best_dist:
            best_dist = meilleure_route.distance
            best_chemin = meilleure_route.chemin
        # Tracer le chemin
        liste_x = []
        liste_y = []
        for ville in meilleure_route.chemin:
            liste_x.append(ville.lng)
            liste_y.append(ville.lat)
        for line in ax.lines:
            line.remove()
        ax.plot(liste_x,liste_y,color='blue',linestyle='dashed')
        canvas.draw()
        # Fenêtre avec informations 
        resultats.insert(tk.END, f"Génération {generation + 1}, Plus petite distance: {meilleure_route.distance:.2f}, Meilleure OAT: {best_dist} , Chemin : {meilleure_route.chemin_trad}" + "\n")
        resultats.see(tk.END)
        fenetre2.update() 

    # Le meilleur pour la fin
    liste_x = []
    liste_y = []
    for ville in best_chemin:
        liste_x.append(ville.lng)
        liste_y.append(ville.lat)
        
    # Retour à la ville de départ
    liste_x.append(best_chemin[0].lng)
    liste_y.append(best_chemin[0].lat)

    for line in ax.lines:
        line.remove()
    ax.plot(liste_x, liste_y, color='yellow', linestyle='dashed')
    canvas.draw()

    # Affichage du chemin final correct
    chemin_names = [ville.name for ville in best_chemin] + [best_chemin[0].name]  # cycle complet
    resultats.insert(tk.END, f"Plus petite distance OAT: {best_dist:.2f}, Chemin : {chemin_names}" + "\n")


def rafraichir():
    """
        Cette méthode permet d'effacer tout le contenu de la fenêtre
    """
    ax.clear()
    depart.destroy()
    listeVilles.destroy()
    gen.destroy()
    select_gen.destroy()
    canvas.draw()

def bouger_cam(event):
    step_ratio = 0.1  # 10% du cadre visible

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    dx = (xlim[1] - xlim[0]) * step_ratio
    dy = (ylim[1] - ylim[0]) * step_ratio

    if event.keysym == 'Left':
        ax.set_xlim(xlim[0] - dx, xlim[1] - dx)
    elif event.keysym == 'Right':
        ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
    elif event.keysym == 'Up':
        ax.set_ylim(ylim[0] + dy, ylim[1] + dy)
    elif event.keysym == 'Down':
        ax.set_ylim(ylim[0] - dy, ylim[1] - dy)

    canvas.draw()


def zoom(event):
    if event.char.lower() == 'e':
        base_scale = 1.2

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Centre actuel de l'affichage
        center_x = (xlim[0] + xlim[1]) / 2
        center_y = (ylim[0] + ylim[1]) / 2

        # Mise à l'échelle
        scale = 1 / base_scale

        new_width = (xlim[1] - xlim[0]) * scale
        new_height = (ylim[1] - ylim[0]) * scale

        ax.set_xlim([center_x - new_width / 2,center_x + new_width / 2])
        ax.set_ylim([center_y - new_height / 2,center_y + new_height / 2 ])

        canvas.draw()

# DEZOOM quand on appuie sur 'A'
def unzoom(event):
    if event.char.lower() == 'a':
        base_scale = 1.2

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Centre actuel de l'affichage
        center_x = (xlim[0] + xlim[1]) / 2
        center_y = (ylim[0] + ylim[1]) / 2

        # Mise à l'échelle
        scale = 1 / base_scale

        new_width = (xlim[1] - xlim[0]) / scale
        new_height = (ylim[1] - ylim[0]) / scale

        ax.set_xlim([center_x - new_width / 2, center_x + new_width / 2])
        ax.set_ylim([center_y - new_height / 2,center_y + new_height / 2])

        canvas.draw()

# Pour qu'on puisse utiliser les touches 
fenetre.bind("<e>", zoom)
fenetre.bind("<a>", unzoom)
fenetre.bind("<Key>", bouger_cam)

fig, ax = plt.subplots(figsize=(6, 5))
canvas = FigureCanvasTkAgg(fig, master=fenetre)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

bouton_frame = tk.Frame(fenetre)
bouton_frame.pack(pady=10)
bouton = tk.Button(bouton_frame, text="1 - Générer la carte", command=lambda : generer_carte()) 
# Bouton lançant la génération de villes
bouton2 = tk.Button(bouton_frame, text="3 - Effacer tout", command = lambda : rafraichir())
# Bouton lançant le rafraichissement de la carte
bouton3 = tk.Button(bouton_frame, text="2 - Lancer l'algo", command = lambda : algo())
# Bouton lançant l'algorithme de parcours

cam.grid(row=1, column=0, padx=10)
zooming.grid(row=1, column=1, padx=10)
nombre.grid(row=0, column=1, padx=10)
scroll.grid(row=1, column=1, padx=10)
pays.grid(row=0, column = 0, padx=10)
liste.grid(row=1, column = 0, padx=10)
bouton.grid(row=0, column=0, padx=10)
bouton2.grid(row=2, column=0, padx=10)
bouton3.grid(row=1, column=0, padx=10)


fenetre.mainloop()
