
# Rapport de projet

## Groupe
* Baris Kaftancioglu 28711733
* Ilyes Djerfaf 

## Description des choix importants d'implémentation

Blablabla

## Description des stratégies proposées

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
Ce joueur s'applique l'algorithme minimax afin de trouver configuration possible qui augmente la distance l'adversaire et son objectif
et minimise lui-même et son ojectif.
Si le joueur est plus proche à son objectif, il s'avance dans son path.

### - Strat 6
Ce joueur s'applique l'algorithme alphabeta afin de trouver configuration possible qui augmente la distance l'adversaire et son objectif
et minimise lui-même et son ojectif.
Si le joueur est plus proche à son objectif, il s'avance dans son path.


## Description des résultats
Dans le matrice,la ligne nous montre le joueur 0 et le colonne nous montre le joueur 1. \
Après la science de statistique, on en déduit 30 jeux est suffisant pour observer la relation entre 2 joueurs.



$$

\begin{matrix}
  & Strat 1 & Strat 2 & Strat 3 & Strat 4 & Strat 5 & Strat 6 & Strat 7 \\ 
  Strat 1 & 13/17 & 6/24 & 2/28 & 3/27 & 0/30 & 0/30 & 0/30  \\ 
  Srat 2 & 25/5 & 21/9 & 11/19 & 8/22 & 0/30 & 0/30 & 0/30 \\
  Strat 3 & 25/5 & 16/14 & 16/14 & 19/11 & 0/30 & 0/30 & 0/30 \\
  Strat 4 & 26/4 &  23/7 & 22/8 & 16/14 & 0/30 & 0/30 & 0/30  \\
  Strat 5 & 30/0 & 30/0 & 30/0 & 30/0 & * & * & * \\
  Strat 6 & 30/0 & 30/0 & 30/0 & 30/0 & * & * & * \\
  Strat 7 & 30/0 & 30/0 & 30/0 & 30/0 & * & * & * 
\end{matrix}

$$

Les éléments avec *  ont toujours le même résultat car les IAs décident de même façon dans chaque jeu.
Donc les résultats ne sont pas définitifs.