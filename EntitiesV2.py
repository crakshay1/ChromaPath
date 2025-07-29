import math
import random

class Ville():
    def __init__(self, name:str, lng: float, lat: float):
        self.name = name
        self.lng = lng
        self.lat = lat

    def get_distance(self, ville):
        """
            Obtient la distance entre deux villes données.
        """
        return math.sqrt((ville.lat-self.lat)**2 + (ville.lng-self.lng)**2)
    
    def get_next_ville(self, liste_villes: list):
        """
            Choisit aléatoirement la prochaine ville à atteindre.
        """
        return random.choice(liste_villes)


class Route():
    def __init__(self, depart, liste_villes: list):
        self.distance = 0 
        self.fitness = 0   
        self.depart = depart
        self.mutation = 0.1
        self.liste_villes = liste_villes
        self.chemin = [depart]
        self.chemin_trad = []
        self.next = depart.get_next_ville(liste_villes)
    
    def trace_ma_route(self):
        """
            Initie la création d'un individu.
        """
        while len(self.chemin) < len(self.liste_villes):
            if self.next in self.chemin:
                self.next = self.depart.get_next_ville(self.liste_villes)
                continue # On évite de rajouter la ville comme doublon
            self.chemin.append(self.next)
            self.depart = self.next
            self.next = self.depart.get_next_ville(self.liste_villes)
        self.chemin.append(self.chemin[0])  # Ferme le cycle

    def get_villes(self):
        """
            Obtient les noms des villes d'une route.
        """
        self.chemin_trad = [ville.name for ville in self.chemin]

    def stack_la_distance(self):
        """
            Permet d'accumuler toutes les distances intervilles.
        """
        self.distance = 0
        for i in range(len(self.chemin)-1):
            villeA = self.chemin[i]
            villeB = self.chemin[i+1]
            self.distance += villeA.get_distance(villeB)

    def evaluer(self):
        """
            L'inverse de la distance est la fitness
            (donc plus facilement interprétable).
        """
        if self.distance == 0:
            self.fitness = 0
        else:
            self.fitness = 1/self.distance
            
    def muter(self) -> list:
        """
            On permute ici deux villes de manière random.
        """
        if random.random() < self.mutation:
            i, j = random.sample(range(len(self.chemin) - 1), 2)  # on exclut le dernier
            self.chemin[i], self.chemin[j] = self.chemin[j], self.chemin[i]
            self.chemin[-1] = self.chemin[0]  # refermer proprement le cycle
        return self.chemin


class Population():
    def __init__(self, liste_chemins: list, depart, liste_villes: list):
        self.chemins = liste_chemins
        self.depart = depart
        self.villes = liste_villes

    def election(self) -> list:
        """
            Elit l'individu au meilleur fitness
            de chaque génération.
        """
        max = self.chemins[0]
        for element in self.chemins:
            element.stack_la_distance()
            element.evaluer()
            if element.fitness > max.fitness:
                max = element
        return element

    def tournoi(self) -> list:
        """
            Permet de choisir des parents via un tournoi.
        """
        taille_tournoi = len(self.chemins)//20
        participants = random.sample(self.chemins, taille_tournoi)
        gagnant = participants[0]
        for chemin in participants: 
            chemin.stack_la_distance()
            chemin.evaluer()
            if chemin.fitness > gagnant.fitness : 
                gagnant = chemin
        return gagnant

    def reproduction(self, parent1, parent2) -> list:
        """
            Effectue un croisement entre deux routes parents
            passés en paramètres.
        """
        taille = len(parent1.chemin) - 1  # exclut la dernière ville (cycle)
        debut = random.randint(0, taille - 2)
        fin = random.randint(debut + 1, taille - 1)

        enfant = [None] * taille
        enfant[debut:fin+1] = parent1.chemin[debut:fin+1]

        index_parent2 = 0
        for i in range(taille):
            if enfant[i] is None:
                while parent2.chemin[index_parent2] in enfant:
                    index_parent2 += 1
                enfant[i] = parent2.chemin[index_parent2]
        enfant.append(enfant[0])  # referme le cycle
        return enfant
    
    def generer_nouvelle_population(self) -> list:
        """
            Génère une nouvelle population en utilisant 
            la sélection, le croisement et la mutation.
        """
        nouvelle_population = []
        for i in range(len(self.chemins)):
            parent1 = self.tournoi() # Une route parent
            parent2 = self.tournoi()
            enfant_liste = self.reproduction(parent1, parent2) # Chemin pour l'enfant
            enfant = Route(self.depart, self.villes) # La route enfant
            enfant.chemin = enfant_liste # Le chemin devient la route enfant
            enfant.muter() # Est-ce que le chemin va muter?
            parent1.evaluer()
            parent2.evaluer()
            enfant.evaluer()
            eva1, eva2, eva3 = parent1.distance, parent2.distance, enfant.distance
            maxi = min([eva1,eva2,eva3])
            if maxi == eva1 :
                nouvelle_population.append(parent1)
            elif maxi == eva2 :
                nouvelle_population.append(parent2)
            else:
                nouvelle_population.append(enfant)

        self.chemins = nouvelle_population
