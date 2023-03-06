# -*- coding: utf-8 -*-

# Nicolas, 2021-03-05
from __future__ import absolute_import, print_function, unicode_literals

import random 
import numpy as np
import sys
from itertools import chain


import pygame

from pySpriteWorld.gameclass import Game,check_init_game_done
from pySpriteWorld.spritebuilder import SpriteBuilder
from pySpriteWorld.players import Player
from pySpriteWorld.sprite import MovingSprite
from pySpriteWorld.ontology import Ontology
import pySpriteWorld.glo

from search.grid2D import ProblemeGrid2D
from search import probleme








# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    name = _boardname if _boardname is not None else 'mini-quoridorMap'
    game = Game('./Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 5  # frames per second
    game.mainiteration()
    player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
    
    nbLignes = game.spriteBuilder.rowsize
    nbCols = game.spriteBuilder.colsize
    assert nbLignes == nbCols # a priori on souhaite un plateau carre
    lMin=2  # les limites du plateau de jeu (2 premieres lignes utilisees pour stocker les murs)
    lMax=nbLignes-2 
    cMin=2
    cMax=nbCols-2
   
    
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    
       
           
    # on localise tous les états initiaux (loc du joueur)
    # positions initiales des joueurs
    initStates = [o.get_rowcol() for o in players]
    ligneObjectif = (initStates[1][0],initStates[0][0]) # chaque joueur cherche a atteindre la ligne ou est place l'autre 
    print(ligneObjectif)
    
    # on localise tous les murs
    # sur le layer ramassable    
    walls = [[],[]]
    walls[0] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == 0 or o.get_rowcol()[0] == 1)]  
    walls[1] = [o for o in game.layers['ramassable'] if (o.get_rowcol()[0] == nbLignes-2 or o.get_rowcol()[0] == nbLignes-1)]  
    allWalls = walls[0]+walls[1]
    nbWalls = len(walls[0])
    assert len(walls[0])==len(walls[1]) # les 2 joueurs doivent avoir le mm nombre de murs
    
    #-------------------------------
    # Fonctions permettant de récupérer les listes des coordonnées
    # d'un ensemble d'objets murs ou joueurs
    #-------------------------------
    
    def wallStates(walls): 
        # donne la liste des coordonnees dez murs
        return [w.get_rowcol() for w in walls]
    
    def playerStates(players):
        # donne la liste des coordonnees dez joueurs
        return [p.get_rowcol() for p in players]
    
   
    #-------------------------------
    # Rapport de ce qui est trouve sut la carte
    #-------------------------------
    print("lecture carte")
    print("-------------------------------------------")
    print("lignes", nbLignes)
    print("colonnes", nbCols)
    print("Trouvé ", nbPlayers, " joueurs avec ", int(nbWalls/2), " murs chacun" )
    print ("Init states:", initStates)
    print("-------------------------------------------")

    #-------------------------------
    # Carte demo 
    # 2 joueurs 
    # Joueur 0: place au hasard
    # Joueur 1: A*
    #-------------------------------
    
        
    #-------------------------------
    # On choisit une case objectif au hasard pour chaque joueur
    #-------------------------------
    
    allObjectifs = ([(ligneObjectif[0],i) for i in range(cMin,cMax)],[(ligneObjectif[1],i) for i in range(cMin,cMax)])
    print("Tous les objectifs joueur 0", allObjectifs[0])
    print("Tous les objectifs joueur 1", allObjectifs[1])
    objectifs =  [allObjectifs[0][random.randint(cMin,cMax-3)], allObjectifs[1][random.randint(cMin,cMax-3)]]
    print("Objectif joueur 0 choisi au hasard", objectifs[0])
    print("Objectif joueur 1 choisi au hasard", objectifs[1])

    #-------------------------------
    # Fonctions definissant les positions legales et placement de mur aléatoire
    #-------------------------------
    def is_okay_path_A_star(player,posPlayers, row,col,wall_curr):
    
        g =np.ones((nbLignes,nbCols),dtype=bool)  # une matrice remplie par defaut a True  
        for w in wall_curr:            # on met False quand murs
            g[w]=False
        g[row][col] = False # on rajoute le positionenement du nouveau mur
        for i in range(nbLignes):                 # on exclut aussi les bordures du plateau
            g[0][i]=False
            g[1][i]=False
            g[nbLignes-1][i]=False
            g[nbLignes-2][i]=False
            g[i][0]=False
            g[i][1]=False
            g[i][nbLignes-1]=False
            g[i][nbLignes-2]=False
        
        p = ProblemeGrid2D(posPlayers[player],objectifs[player],g,'manhattan')
        path = probleme.astar(p,verbose=False)

        print("IS OKAY PATH",path)
        
        return path[-1]==objectifs[player] and posPlayers[player] not in path[1:]


    def legal_wall_position(pos, player, posPlayers,wall_curr):
        row,col = pos
        # une position legale est dans la carte et pas sur un mur deja pose ni sur un joueur
        # attention: pas de test ici qu'il reste un chemin vers l'objectif

        # on ajoute le test ici qu'il rest un chemin vers l'objectif
        if((pos not in wallStates(allWalls)) and (pos not in playerStates(players)) and row>lMin and row<lMax-1 and col>=cMin and col<cMax):
            return is_okay_path_A_star(1-player,posPlayers, row, col,wall_curr) and is_okay_path_A_star(player,posPlayers, row, col,wall_curr)
        return False

    
    def draw_random_wall_location(player, posPlayers):
        # tire au hasard un couple de position permettant de placer un mur
        while True:
            wall_curr=wallStates(allWalls)
            print("WALLL CURR",wall_curr)
            random_loc = (random.randint(lMin,lMax),random.randint(cMin,cMax))
            if legal_wall_position(random_loc, player, posPlayers,wall_curr):
                wall_curr.append(random_loc) 
                inc_pos =[(0,1),(0,-1),(1,0),(-1,0)] 
                random.shuffle(inc_pos)
                for w in inc_pos:
                    random_loc_bis = (random_loc[0] + w[0],random_loc[1]+w[1])
                    if legal_wall_position(random_loc_bis,player, posPlayers,wall_curr):
                        return(random_loc,random_loc_bis)

    ###########################################################################################################################
    ###########################################################################################################################
    ###########################################################################################################################
    ###########################################################################################################################
    ###########################################################################################################################
    ###########################################################################################################################
    def draw_wall_proche(player, posPlayers):
        # tire au hasard un couple de position permettant de placer un mur
        while True:
            wall_curr=wallStates(allWalls)
            print("WALLL CURR",wall_curr)
            random_loc = (posPlayers[1 - player][0],posPlayers[1 - player][1]+1)
            if legal_wall_position(random_loc, player, posPlayers,wall_curr):
                wall_curr.append(random_loc) 
                inc_pos =[(0,1),(0,-1),(1,0),(-1,0)] 
                random.shuffle(inc_pos)
                for w in inc_pos:
                    random_loc_bis = (random_loc[0] + w[0],random_loc[1]+w[1])
                    if legal_wall_position(random_loc_bis,player, posPlayers,wall_curr):
                        return(random_loc,random_loc_bis)

    #-------------------------------
    # Le joueur 0 place tous les murs au hasard
    #-------------------------------
                    
        

   
    
    #-------------------------------
    # calcul A* pour le joueur 1
    #-------------------------------
    

    def calcul_path_A_star(player,posPlayers):
    
        g =np.ones((nbLignes,nbCols),dtype=bool)  # une matrice remplie par defaut a True  
        for w in wallStates(allWalls):            # on met False quand murs
            g[w]=False
        for i in range(nbLignes):                 # on exclut aussi les bordures du plateau
            g[0][i]=False
            g[1][i]=False
            g[nbLignes-1][i]=False
            g[nbLignes-2][i]=False
            g[i][0]=False
            g[i][1]=False
            g[i][nbLignes-1]=False
            g[i][nbLignes-2]=False
        p = ProblemeGrid2D(posPlayers[player],objectifs[player],g,'manhattan')
        path = probleme.astar(p,verbose=False)
        print ("Chemin trouvé:", path)
        return path
    
    def calcul_path_A_star_dynamique(player,posPlayers):
    
        g =np.ones((nbLignes,nbCols),dtype=bool)  # une matrice remplie par defaut a True  
        for w in wallStates(allWalls):            # on met False quand murs
            g[w]=False
        for i in range(nbLignes):                 # on exclut aussi les bordures du plateau
            g[0][i]=False
            g[1][i]=False
            g[nbLignes-1][i]=False
            g[nbLignes-2][i]=False
            g[i][0]=False
            g[i][1]=False
            g[i][nbLignes-1]=False
            g[i][nbLignes-2]=False
        
        p = ProblemeGrid2D(posPlayers[player],objectifs[player],g,'manhattan')
        path_init = probleme.astar(p,verbose=False)

        for obj in allObjectifs[player]:
            p = ProblemeGrid2D(posPlayers[player],obj,g,'manhattan')
            path_dynamique = probleme.astar(p,verbose=False)
            if len(path_dynamique) < len(path_init):
                path_init = path_dynamique
                objectifs[player] = obj
            
        
        print ("Chemin trouvé:", path_init)
        return path_init


    def jouer_aleatoire(player, walls_used):
        """stratégie aléatoire ou les deux joeurs ont le choix entre avancer ou placer un mur aléatoirement 
        """
        choix_du_jouer=random.choice([0,1])

        if choix_du_jouer==0:
            if walls_used[player]>=10:
                choix_du_jouer=1
            else:
                wall_to_remplir=walls_used[player]
                ((x1,y1),(x2,y2)) = draw_random_wall_location(player, posPlayers)
                walls[player][wall_to_remplir].set_rowcol(x1,y1)
                walls[player][wall_to_remplir+1].set_rowcol(x2,y2)
                walls_used[player]=walls_used[player]+2

        
        # on fait bouger le joueur 1 jusqu'à son but
        # en suivant le chemin trouve avec A* 
        if choix_du_jouer==1: #Il a choisi joueur
            path=calcul_path_A_star(player,posPlayers)
            row,col = path[1]
            posPlayers[player]=(row,col)
            players[player].set_rowcol(row,col)
            #print ("pos joueur",player,":",row,col)
            if (row,col) == objectifs[player]:
                print("le joueur",player,"a atteint son but!")
                return True, player
            
        return False, player

    def jouer_aleatoire_avance(player, walls_used):
        """stratégie aléatoire avancée
        
        si le jouer est proche du cible on doit avancer et non pas constuire un mur aléatoirement
        """

        # calcul de la longeur du path pour les deux joeurs :
        choix_du_jouer = 1 if len(calcul_path_A_star(player,posPlayers)) < len(calcul_path_A_star(1 - player,posPlayers)) else 0

        if choix_du_jouer==0:
            if walls_used[player]>=10:
                choix_du_jouer=1
            else:
                wall_to_remplir=walls_used[player]
                ((x1,y1),(x2,y2)) = draw_random_wall_location(player, posPlayers)
                walls[player][wall_to_remplir].set_rowcol(x1,y1)
                walls[player][wall_to_remplir+1].set_rowcol(x2,y2)
                walls_used[player]=walls_used[player]+2

        
        # on fait bouger le joueur 1 jusqu'à son but
        # en suivant le chemin trouve avec A* 
        if choix_du_jouer==1: #Il a choisi joueur
            path=calcul_path_A_star(player,posPlayers)
            row,col = path[1]
            posPlayers[player]=(row,col)
            players[player].set_rowcol(row,col)
            #print ("pos joueur",player,":",row,col)
            if (row,col) == objectifs[player]:
                print("le joueur",player,"a atteint son but!")
                return True, player
            
        return False, player

    
    def jouer_objectif_proche(player, walls_used):
        """stratégie aléatoire avancée
        
        si le jouer est proche du cible on doit avancer et non pas constuire un mur aléatoirement
        """

        # calcul de la longeur du path pour les deux joeurs :
        choix_du_jouer = 1 if len(calcul_path_A_star(player,posPlayers)) < len(calcul_path_A_star(1 - player,posPlayers)) else 0

        if choix_du_jouer==0:
            if walls_used[player]>=10:
                choix_du_jouer=1
            else:
                wall_to_remplir=walls_used[player]
                ((x1,y1),(x2,y2)) = draw_random_wall_location(player, posPlayers)
                walls[player][wall_to_remplir].set_rowcol(x1,y1)
                walls[player][wall_to_remplir+1].set_rowcol(x2,y2)
                walls_used[player]=walls_used[player]+2

        
        # on fait bouger le joueur 1 jusqu'à son but
        # en suivant le chemin trouve avec A* 
        if choix_du_jouer==1: #Il a choisi joueur
            path=calcul_path_A_star_dynamique(player,posPlayers)
            row,col = path[1]
            posPlayers[player]=(row,col)
            players[player].set_rowcol(row,col)
            #print ("pos joueur",player,":",row,col)
            if (row,col) == objectifs[player]:
                print("le joueur",player,"a atteint son but!")
                return True, player
            
        return False, player
    
    def jouer_placer_mur_proche(player, walls_used):
        """stratégie aléatoire avancée
        
        si le jouer est proche du cible on doit avancer et non pas constuire un mur aléatoirement
        """

        # calcul de la longeur du path pour les deux joeurs :
        choix_du_jouer = 1 if len(calcul_path_A_star(player,posPlayers)) < len(calcul_path_A_star(1 - player,posPlayers)) else 0

        if choix_du_jouer==0:
            if walls_used[player]>=10:
                choix_du_jouer=1
            else:
                wall_to_remplir=walls_used[player]
                ((x1,y1),(x2,y2)) = draw_wall_proche(player, posPlayers)
                walls[player][wall_to_remplir].set_rowcol(x1,y1)
                walls[player][wall_to_remplir+1].set_rowcol(x2,y2)
                walls_used[player]=walls_used[player]+2

        
        # on fait bouger le joueur 1 jusqu'à son but
        # en suivant le chemin trouve avec A* 
        if choix_du_jouer==1: #Il a choisi joueur
            path=calcul_path_A_star_dynamique(player,posPlayers)
            row,col = path[1]
            posPlayers[player]=(row,col)
            players[player].set_rowcol(row,col)
            #print ("pos joueur",player,":",row,col)
            if (row,col) == objectifs[player]:
                print("le joueur",player,"a atteint son but!")
                return True, player
            
        return False, player


    def placer_les_murs_intelligement(player):
        legal_walls=[]
        for i in range(lMin,lMax):
            for j in range(cMin,cMax):
                voisins=[(0,1),(0,-1),(1,0),(-1,0)]
                for v in voisins:
                    if legal_wall_position((i,j), player, posPlayers,allWalls) and legal_wall_position((v[0]+i,v[1]+j), player, posPlayers,allWalls):
                        if ((i,j),(i+v[0],j+v[1])) not in legal_walls:
                            legal_walls.append((i,j),(i+v[0],j+v[1]))

        
          
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
            
    posPlayers = initStates

    print(iterations)


    walls_used=[0,0]
    for i in range(iterations):

        player=2
        if i%2==0:
            player=0
        else:
            player=1

        # print("Le joueur actuel :",player)
        
        end,gagnat = jouer_aleatoire(player, walls_used) if player == 0 else jouer_placer_mur_proche(player, walls_used)    
        if end:
            return gagnat
        
        # mise à jour du pleateau de jeu
        game.mainiteration()
        # print(walls_used)
    
    pygame.quit()
    
    
    
    
    #-------------------------------
    
        
    
    
from collections import Counter

if __name__ == '__main__':
    #gagnat = []
    #for i in range(0,30):
    #    gagnat.append(main())
    #
#
    #count = Counter(gagnat)
    #most_common_element = count.most_common(1)[0][0]
    #print(most_common_element)

    main()
    


