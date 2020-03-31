# deep-ail
Projet IA - Centrale

*par Barrau Stepan, Biddulph Owain, Delattre Julien, Goualard François, Topuz Nicolas*

## Contexte et objectif du projet 

L'objectif de ce projet est de concevoir un système capable de jouer une partie de Loup-garou contre Vampire en vue de disputer un tournoi. Il s'agit d'un jeu de plateau tour par tour opposant deux équipes. Celles-ci peuvent déplacer leurs troupes en groupe ou en les séparant. Elles peuvent augmenter leurs effectifs en vainquant les humains présents sur le terrain. Les deux équipes peuvent se battre selon des règles d'engagement spécifiques. Enfin, l'équipe avec le plus grand effectif à la fin de la partie l'emporte. 

Dans le cadre du tournoi, chaque instruction pour un coup doit être calculée en un temps inférieur à deux secondes, puis être envoyé au serveur selon un format particulier. Les coups de l'adversaire sont reçus depuis le serveur selon le même format. 

## Installation et lancement

Pour utiliser notre IA, télécharger le repository et après avoir lancé le programme du serveur, vous pouvez finalement démarrer notre joueur (et la partie si tant est qu'il y ait un deuxième joueur) en exécutant depuis la root la commande :
```python main.py ip port``` 

## Approche du problème

Notre intuition première a consisté à nous diriger vers une IA à heuristique fonctionnant grâce à un algorithme alpha-beta, orientant ainsi la majorité de la structure de notre code. Toutefois nos avancées nous ont fait prendre conscience de la nécessité de prendre en compte plusieurs phases du jeu afin de nous adapter au mieux au contexte. 

Nous avons ainsi distingué : 
- Une première phase qui dure jusqu'à ce que tous les humains aient été absorbé. Dans cette phase, le but des équipes est de grossir autant que possible pour obtenir l'avantage sur leurs adversaires en mangeant des humains sans risquer de perdre des troupes face à l'adversaire. 
- A la disparition des derniers humains démarre donc une deuxième phase où l'objectif principal est de regrouper ces troupes. En effet à ce stade, chaque équipe a atteint sa taille maximale, il faut donc (sauf opportunité intéressante de réduire le nombre d'adversaires) tâcher de rassembler ses troupes afin de diminuer les risques de se faire manger. 
- Une fois ses troupes regroupées, démarre la troisième et dernière phase de fin de partie qui néssecite, nous le verrons, une approche un peu différente.

Les deux premières phases ont été implémentées avec un algorithme alpha-beta tandis que la troisième prend la forme d'un système "expert". Ce sont ces différents éléments ainsi que la volonté d'être le plus rapide pour déterminer un coup à venir (et ainsi potentiellement augmenter notre profonder de recherche d'état) qui ont déterminé la structure de notre code et notre implémentation.

### Structure du code 

Le code est construit autour du fichier ```main.py``` qui instancie un joueur en la présence d'un client socket qui traite les messsages reçus du serveur et en renvoie quand c'est nécessaire. Ce client est défini dans le fichier ```client.py```. Il fait ensuite appel au fichier ```response.py``` qui définit la réponse à mettre en place en faisant appel au programme alpha-beta défini dans le fichier éponyme, avec l'heuristique défini dans le dossier ```heuristic``` et avec la modélisation du plateau de jeu réalisé grâce aux éléments du fichier ```state.py```.

### Détails particuliers de l'implémentation

L'implémentation du programme alpha-beta repose sur une structure assez classique. Nous avons toutefois ajouté quelques particularités afin de gagner en vitesse de parcours des états : 
- L'implémentation des heuristiques à travers une classe de manière à garder un cache des états parcourus pour gagner du temps lors de l'évaluation de ceux-ci (voir ```heuristics\basic.py```).
- Un tri préalable des états à parcourir (d'abord les états passsant par un combat contre des humains, puis les états avec fusion de groupe de l'espèce, puis ceux avec combat contre l'ennemi et enfin ceux impliquant un déplacement sur des cases vides) de manière à effectuer les mouvements critiques en priorité (voir ```alphabeta.py```).
- L'implémentation des espèces à travers des classes de manière à faire évoluer les informations qui leur sont relatives à chaque réception de changement sans avoir à reparcourir à chaque fois l'ensemble du plateau de jeu (voir ```state.py```).
- Une class *GlobalStrategy* permet de faire baisser la profondeur de l’alphabeta si les calcules prennent trop de temps.

### Explication de la stratégie adoptée 


Comme expliqué ci-dessus, nous avons décomposer la partie en trois temps :

- Le début de partie où il faut grandir aussi vite que possible.   

  Cette partie-là est assez naturellement gérée via une heuristique, composée de plusieurs scores qui étaient dans un premier temps au nombre de deux : un score évaluant les tailles respectives des deux équipes en faisant leur différence, un score évaluant le potentiel de l'équipe en considérant la distance aux autres groupes présents et en pondérant celle-ci par la probabilité de victoire en cas de combat si on est sur-numéraire et par moins la probabilité de victoire si on est sous-numéraire (de manière à avoir un système qui évite les combats idéalement et privilégie les victoires faciles lui permettant de grossir facilement).  
  
  L'avantage de ce dernier score est qu'il permettait quand même de prendre en compte les éléments lointains sans pour autant nécessiter une profondeur d'exploration trop importante. C'était également une de ces faiblesses : si deux groupes adverses se dirigeaient tout deux vers un même groupe d'humain qu'ils atteindraient au-delà de la profondeur d'exploration de l'alpha-beta, un des deux "perdaient" plusieurs coup à s'approcher d'un groupe qu'il ne mangerait jamais (ne s'en rendant compte que lorsqu'il est à uns distance inférieur de la profondeur d'exploration du groupe cible). C'est ce constat qui nous a motivé à ajouter un troisième score de compétition permettant de détecter ce genre de situation et ne pas se diriger vers un groupe situé plus proche d'un de nos groupes ou d'un groupe adverse.
  
  
- Le milieu de partie où il n'y a plus d'humain où le but est alors de rassembler ces troupes pour ne pas les laisser vulnérables de manière inutiles.  

  Cette partie-là est également gérée via une heuristique légèrement différente de la précédente : on garde le premier score évaluant les tailles des équipes (car cela reste le nerf de la guerre et on ne voudrait pas passer à côté d'un groupe adverse qu'on est sûr de vaincre sans le faire) auquel on ajoute un malus pour le nombre de groupes qu'on a de manière à encourager le système à les regrouper en un seul groupe.  
  
  
- La fin de partie, une fois nos troupes regroupées.  
  
  A ce stade, comme il n'y a plus d'humain, les cartes sont jouées et on rencontre plusieurs cas de figure. Si on est 1,5 fois plus nombreux que les adversaires, nous avons gagné quoiqu'il arrive, il faut juste nous assurer de ne pas timeout. Si on est 1,5 fois moins que les adversaires, il n'y a rien que l'on puisse faire si ce n'est essayer de le faire timeout (à cette fin, on essaiera de se splitter autant que possible en maintenant nos troupes équidistantes de l'adversaire). Sinon il faut gérer le conflit aléatoire en gardant en tête que l'attaque est toujours plus avantageuse que la défense à configuration fixée.  

  Dès lors, si on est en supériorité numérique, on tâchera d'éviter le conflit puis d'attaquer lorsqu'il n'y a plus le choix. Si on est infériorité numérique, il nous faudra donc tâcher d'attaquer en s'assurant d'être l'attaquant. Ces mouvements étant plus complexes à faire comprendre et présentant des cas où il faut prendre des actions dont il résultera potentiellement quelque chose de moins bon que la situation précédente, une heuristique semble peu adaptée à ce cas et nous avons donc choisi une implémentation basée sur un système expert. Le système expert est là pour décider du cas de figure dans lequel on se trouve, et déduire la meilleure stratégie. Les stratégies sont implémentées soit par un alpha-beta avec une heuristique spécifique, soit simplement hard-codées. Le système expert reste très simple, il n'y a que trois règles, car la situation est simple. Finalement, il aurait été possible d'implémenter le choix de la stratégie sous la forme d'un agent réflexe, mais nous avons voulu implémenter le système expert, au moins pour la beauté du geste. 

Cas particulier enfin : la gestion du split. En effet, le fait de savoir quand nos troupes doivent se séparer est crucial dans certains cas pour l'emporter mais conduit néanmoins à une véritable explosion combinatoire si on n'y prête pas attention. Nous avons donc fait plusieurs choix :
- Tout d'abord, nous avons considéré qu'il n'est intéressant de se splitter qu'en vu d'attaquer des groupes de taille inférieure. Par conséquent on n'explore les possibilités de split qu'à partir du moment où nous avons moins de groupe qu'il n'y a de groupes humains ou adverses présents. Qui plus est, même dans ce cas, le split n'est considéré que lorsqu'il y a au moins deux groupes présentant des tailles respectivement inférieures à celles des sous-groupes ainsi formés. 
- Nous avons ensuite considéré qu'un split se faisait toujours en vue d'un objectif. Ainsi nous forçons ensuite le placement des groupes splittés plutôt que de considérer l'ensemble des combinaisons de 2 parmi 8 en ciblant les deux groupes de taille inférieures les plus proches de nos troupes.
- Nous avons considéré que tous les groupes résultant des splits étaient obligés de bouger, au moins tant qu'il reste des humains. En effet à ce stade, on est dans une situation de course de sorte qu'a priori l'immobilisme n'apporte rien. Cette hypothèse permet de gagner un temps de calcul précieux.

## Perspectives 

Nous avons donc conçu un système capable de se connecter au serveur et de jouer d'une manière qui semble cohérente et que nous sommes impatients de suivre au cours du tournoi. 
A ce stade nous observons quelques limites :
- Des difficultés à expliquer certains comportements a priori lorsqu'on atteint des profondeurs plus élevées.
- La profondeur permet de gagner en performance mais augmente nettement le temps de calcul. Par conséquent, nous avons mis en place des mécanismes pour adapter la profondeur de l'alphabeta en fonction du temps que l'on prend par rapport au temps imparti. Seulement, cette profondeur pourrait être remontée par la suite.
- Nous avons constaté un bugg dans le fonctionneent du système expert : en effet lorsque notre IA se trouve en sous-nombre, non seulement elle ne se split pas comme elle devrait le faire mais lorsqu'elle est dans une situation où elle est sure de perdre elle crash. En effet tous les mouvements possibles ont un score de -inf et ne sont donc pas ajouté au alpha beta qui ne renvoie donc aucun mouvement d'où le crash. Nous n'avons toutefois pas pris le temps de le corriger car cela n'impacte en rien le résultat (situation où nous avons forcément perdu) et nous avons donc choisi de privilégier d'autres problèmes.
- Autre bugg constaté : dans la phase de milieu de partie, l'heuristic end_game_score ne parvient pas à déboucher sur la convergence des troupes de notre IA sans que nous arrivions à l'expliquer. Toutefois nous avons manqué de temps pour identifier le problème et le résoudre.
