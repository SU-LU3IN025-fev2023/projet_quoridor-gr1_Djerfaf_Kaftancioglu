
# Rapport de projet

## Groupe

* **Baris Kaftancioglu 28711733**
* **Ilyes Djerfaf 21215141**

## **Description des choix importants d'implémentation**

### **Minimax**

Le minimax est un algorithme utilisé dans la théorie des jeux pour déterminer la meilleure stratégie à adopter pour un joueur dans un jeu à deux joueurs à somme nulle, c'est-à-dire un jeu où les gains d'un joueur sont les pertes de l'autre joueur et vice versa.

L'algorithme fonctionne en explorant l'arbre de jeu complet à partir de l'état actuel du jeu jusqu'à toutes les possibilités de configurations des murs possibles. Il attribue une valeur à chaque état de jeu en fonction de coup d'évaluation.

Le joueur cherche à maximiser son score de l'évaluation, tandis que l'adversaire cherche à minimiser le score de l'évaluation joueur. Pour chaque état de jeu, le joueur  calcule la valeur maximale de toutes les configurations possibles à partir de cet état, et l'adversaire calcule la valeur minimale de de toutes les configurations possibles à partir de cet état.

À partir de l'état actuel du jeu, l'algorithme minimax examine toutes les possibilités de remplacements des murs possibles jusqu'à un certain niveau de profondeur(horizon), et retourne le meilleur mouvement possible à effectuer pour le joueur.

### **Alpha-Beta**

L'algorithme Alpha-Beta est une extension de l'algorithme Minimax utilisé dans les jeux à deux joueurs avec un arbre de recherche de décision. L'algorithme Alpha-Beta vise à réduire le nombre de nœuds évalués par l'algorithme Minimax en élaguant certaines branches de l'arbre qui ne sont pas pertinentes pour la décision finale.

L'algorithme fonctionne en utilisant deux valeurs : alpha et beta. Alpha est la meilleure valeur connue pour le joueur Max jusqu'à présent, tandis que beta est la meilleure valeur connue pour le joueur Min jusqu'à présent. L'algorithme Alpha-Beta recherche l'arbre de jeu en profondeur en utilisant une approche récursive, en évaluant les nœuds les uns après les autres. Au fur et à mesure que l'algorithme se déplace dans l'arbre, il met à jour les valeurs alpha et beta pour chaque nœud visité.

Lorsque l'algorithme atteint un nœud Max, il met à jour la valeur alpha avec la valeur maximale trouvée jusqu'à présent. Si la valeur alpha est supérieure ou égale à la valeur de beta, l'algorithme peut s'arrêter d'évaluer les autres nœuds de cette branche car le joueur Min ne choisira jamais cette branche car elle est moins intéressante que les autres branches déjà explorées. De même, lorsque l'algorithme atteint un nœud Min, il met à jour la valeur beta avec la valeur minimale trouvée jusqu'à présent. Si la valeur beta est inférieure ou égale à la valeur de alpha, l'algorithme peut s'arrêter d'évaluer les autres nœuds de cette branche car le joueur Max ne choisira jamais cette branche car elle est moins intéressante que les autres branches déjà explorées.

L'utilisation de alpha et beta pour élaguer les branches de l'arbre permet de réduire considérablement le nombre de nœuds évalués par l'algorithme Minimax, ce qui permet une meilleure performance de l'algorithme et une prise de décision plus rapide.

### **MCSTS (Monte Carlo Tree Search with Supervised learning)**

Le principe de base de MCSTS est de construire un arbre de recherche de décision à partir d'un état initial en utilisant MCTS. Cet arbre est alors utilisé pour générer des exemples d'entraînement pour un modèle d'apprentissage supervisé. Le modèle est ensuite utilisé pour prédire les résultats des actions possibles à partir de chaque état.Il fait tourner 10 match entre 2 joueurs aléatoires à partir de l'état actuel.

## **Description des stratégies proposées**

### - Strat 1

Ce joueur joue aléatoirement.

### - Strat 2

Ce joueur remplace des murs dans un façon aléatoire s'il est plus loin à son objectif que son adversaire.
Si le joeur est plus proche à so onbjectif, il s'avance dans son path.

### - Strat 3

Ce joueur remplace des murs dans un façon aléatoire s'il est plus loin à son objectif que son adversaire.
Si le joeur est plus proche à so onbjectif, il s'avance dans son path.
Il change son objectif afin d'avoir l'objectif le plus proche.

### - Strat 4

Ce joueur essaie de mettre les murs dans un façon rendre plus loin l'objectif de son adversaire que celui d'avant mettre les murs.
Si le joueur est plus proche à sn ojectif que son adversaire, il s'avance dans son path.

### - Strat 5

Ce joueur s'applique l'algorithme minimax afin de trouver configuration possible qui augmente la distance de l'adversaire et  objectif de l'adversaire et minimise la distance entre lui-même et son ojectif.
Si le joueur est plus proche à son objectif, il s'avance dans son path.

### - Strat 6

Ce joueur s'applique l'algorithme alphabeta afin de trouver configuration possible qui augmente la distance l'adversaire et l'objectif de son adversaire et minimise la distance entre lui-même et son ojectif.
Si le joueur est plus proche à son objectif, il s'avance dans son path.

### - Strat 7

Ce joueur se base sur MCTS dans chaque état. Il fait tourner 10 match entre 2 joueurs aléatoires à partir de l'état actuel.

## Description des résultats

Dans le matrice,la ligne nous montre le joueur 0 et le colonne nous montre le joueur 1. \
Après la science de statistique, on en déduit 30 jeux est suffisant pour observer la relation entre 2 joueurs.

$$

\begin{matrix}
  & Strat 1 & Strat 2 & Strat 3 & Strat 4 & Strat 5 & Strat 6 & Strat 7 \\ 
  Strat 1 & (13,17) & (6,24) & (2,28) & (3,27) & (0,30) & (0,30) & (0,30)  \\ 
  Strat 2 & (25,5) & (21,9) & (11,19) & (8,22) & (0,30) & (0,30) & (0,30) \\
  Strat 3 & (25,5) & (16,14) & (16,14) & (19,11) & (0,30) & (0,30) & (0,30) \\
  Strat 4 & (26,4) &  (23,7) & (22,8) & (16,14) & (0,30) & (0,30) & (0,30)  \\
  Strat 5 & (30,0) & (30,0) & (30,0) & (30,0) & * & * & * \\
  Strat 6 & (30,0) & (30,0) & (30,0) & (30,0) & * & * & * \\
  Strat 7 & (30,0) & (30,0) & (30,0) & (30,0) & * & * & * 
\end{matrix}

$$

Les éléments avec *  ont toujours le même résultat car les IAs décident de même façon dans chaque jeu.
Donc les résultats ne sont pas définitifs.