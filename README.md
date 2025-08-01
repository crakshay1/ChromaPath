## Introduction
Le Problème du Voyageur de Commerce (TSP) est un problème d’optimisation combinatoire classique.
Il consiste à trouver le plus court chemin permettant à un vendeur de visiter une série de villes une seule fois chacune, avant de revenir à son point de départ.
Ici, l'algorithme génétique est utilisé pour résoudre ce problème.

## Exigences 
Chromapath est un projet conçu sur Python utilisant Matplotlib, Geopandas, et Tkinter. Le fichier requirements.txt montre tous les modules Python requis pour pouvoir exécuter le programme. En effet, une interface graphique générée via Tkinter
permet de visualiser l'execution de l'algorithme génétique sur la carte générée par Matplotlib. Cette carte correspond à un pays dont le fichier .shp est traité par Geopandas. Les informations d'un pays, tels que son nom, ses villes, les coordonnées des villes ont été obtenues par 
des données JSON exploitables sur https://www.geonames.org.

## Fonctionnement de Chromapath
Le problème mentionné dans l'introduction a été illustré via le projet Chromapath. En effet, il permet la sélection d'un pays parmi plus de 130, et la génération d'un nombre de villes N qui sont sélectionnées de manière aléatoire. 
Ces villes sont placées sur la carte avec leurs coordonnées exactes. L'utilisateur a alors la possibilité de lancer l'algorithme afin de trouver une solution au TSP avec les villes générées.
### Lancement de Chromapath
![alt text](https://github.com/crakshay1/ChromaPath/blob/main/Assets/Debut.png)
Au lancement, seules la sélection du pays ainsi que celle du nombre voulu de villes générées sont possibles. Une fois ces sélections faites, il faut cliquer sur le bouton 'Générer la carte'.
### Exécution de l'algorithme génétique
La carte étant générée, il est alors possible de sélectionner une ville de départ et un nombre voulu de générations (soit le nombre de fois que l'algorithme génère une solution au problème; la solution la plus optimale est toujours celle retenue au fil des générations).
Il faut alors cliquer sur 'Lancer l'algo' pour visualiser l'exécution de l'algorithme génétique, une fois les sélections évoquées précédemment sont faites.  
![alt text](https://github.com/crakshay1/ChromaPath/blob/main/Assets/Portugal.gif)  
Les chemins bleus sont les solutions trouvées à chaque génération. Une fois la recherche finie, la solution finale est montrée en jaune.
### Vue d'ensemble sur Chromapath 
![alt text](https://github.com/crakshay1/ChromaPath/blob/main/Assets/Fin.png)  
Voici ce qu'on obtient après l'exécution du programme en choissisant comme pays le Portugal. La petite fenêtre rose permet de faire le résumé de chaque génération lors de l'exécution de l'algorithme génétique.
### Caméra
Les pays étant générés de manière fidèle au monde réel sur Chromapath, certains pays peuvent être moins visibles que d'autres. Il est alors possible de zoomer via E ou de dezoomer via A pour voir ces pays de plus près. De plus, les flèches directionnelles du clavier permettent le déplacement sur la carte, 
afin que l'utilisateur puisse voir ce qu'il se passe même dans les zones les plus petites.  
![alt text](https://github.com/crakshay1/ChromaPath/blob/main/Assets/Maurice.gif)  
Les mouvements de caméra (déplacement, zoom, dezoom) sont possibles même lorsque l'algorithme génétique est en pleine exécution.

