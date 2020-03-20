# deep-ail
IA project Centrale
par Barrau Stepan, Biddulph Owain, Delattre Julien, Goualard François, Topuz Nicolas

## Contexte et objectif du projet 

L'objectif de ce projet est de concevoir un système capable de jouer une partie de Loup-garou contre Vampire en vue de disputer un tournoi. Il s'agit d'un jeu de plateau tout par tour opposant deux équipes. Celles-ci peuvent déplacer leur troupe en groupe ou en les séparant. Elles peuvent augmenter leurs effectifs en vainquant les humains présents sur le terrain. Les deux équipes peuvent se battre selon des règles d'engagement spécifiques. Enfin l'équipe avec le plus d'effectif à la fin de la partie l'emporte. 

Dans le cadre du tournoi, chaque instruction pour un coup doit être calculé en un temps inférieur à 2s puis être envoyé au serveur selon un format particulier. Les coups de l'adversaire sont reçus depuis le serveur selon le même format. 

## Installation et lancement - à modifier une fois proprement packagé 

Pour utiliser notre IA, télécharger le repository et après avoir lancé le programme du serveur, vous pouvez finalement démarrer notre joueur (et la partie si tant est qu'il y a un deuxième joueur) en exécutant depuis la root la commande :
```python main``` 

## Approche du problème

Notre intuition première a consister à nous diriger vers une IA à heuristique fonctionnant grâce à un algorithme alpha-beta, orientant ainsi la majorité de la structure de notre code. Toutefois nos avancées nous ont fait prendre conscience de la nécessité de prendre en compte plusieurs phases du jeu afin de nous adapter au mieux au contexte. 

Nous avons ainsi distingué : 
- une première phase durant jusqu'à ce que tous les humains a été absorbé. Dans cette phase le but des équipes est de grossir autant que possible pour obtenir l'avantage sur leurs adversaires en mangeant des humains sans risquer de perdre des troupes à l'adversaire. 
- à la disparition des derniers humains démarre donc une deuxième phase où l'objectif principal est de regrouper ces troupes. En effet à ce stade, chaque équipe a atteint sa taille maximale, il faut donc (sauf opportunité intéressante de réduire le nombre d'adversaires) tâcher de rassembler ces troupes afin de diminuer les risques de se faire manger. 
- enfin un fois ces troupes regroupées, démarre la troisième et dernière phase de fin de partie qui néssecite, nous le verrons, une approche un peu différente

Les deux premières phases ont été implémentées avec un algorithme alpha-beta tandis que la troisième prend la forme d'un système "expert". Ce sont ces différents éléments ainsi que la volonté d'être le plus rapide pour déterminer un coup à venir (et ainsi potentiellement augmenter notre profonder de recherche d'état) qui ont déterminé la structure de notre code et notre implémentation.

### Structure du code 

Le code est construit autour du fichier ```main.py``` qui instancie un joueur en la présence d'un client socket qui traite les messsages reçus du serveur et en renvoie quand c'est nécessaire. Ce client est défini dans le fichier ```client.py```. Il fait ensuite appelle au fichier ```response.py``` qui définit la réponse à mettre en place en faisant appel au programme alpha-beta défini dans le fichier éponyme, avec l'heuristique défini dans le dossier ```heuristic``` et avec la modélisation du plateau de jeu réalisé grâce aux éléments du fichier ```state.py```.

### Détails particuliers de l'implémentation

L'implémentation du programme alpha-beta repose sur une structure assez classique. Nous avons toutefois ajouté quelque particularité afin de gagner en vitesse de parcour des états : 
- l'implémentation de l'heuristique à travers une classe de manière à garder un cache des états parcourus pour gagner du temps lors de l'évaluation de ceux-ci (voir ```heuristics\basic.py```)
- un tri préalable des états à parcourir (d'abord les états passsant par un combat contre des humains, puis les états avec fusion de groupe de l'espèce, puis ceux avec combat contre l'ennemi et enfin ceux impliquant un déplacement sur des cases vides) de manière à effectuer les mouvements critiques en priorité (voir ```alphabeta.py```)
- l'implémentation des espèces à travers des classes de manière à faire évoluer les informations qui leur sont relatives à chaque réception de changement sans avoir à reparcourir à chaque fois l'ensemble du plateau de jeu (voir ```state.py```)


### Explication de la stratégie adoptée 

## Perspectives 
