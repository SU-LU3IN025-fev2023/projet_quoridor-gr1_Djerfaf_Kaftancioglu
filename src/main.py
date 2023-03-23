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

import tkinter as tk


def welcome_frame():


    # create a window
    # Création de la fenêtre principale
    root = tk.Tk()
    root.title("Quridor")
    root.geometry("500x400")

    # Titre principal
    title = tk.Label(root, text="WELCOME to Quridor", font=("Arial", 24))
    title.pack(pady=20)

    # Texte et boutons pour la sélection de la stratégie du joueur 1
    label_strat1 = tk.Label(root, text="Select the Strategy for Player 1 :")
    label_strat1.pack()
    strat1 = tk.StringVar()
    strat1.set("Strat 1")  # Stratégie par défaut
    strat1_buttons = tk.Frame(root)
    strat1_buttons.pack()
    for i in range(1, 8):
        button = tk.Radiobutton(strat1_buttons, text="Strat " +
                                str(i), variable=strat1, value="Strat " + str(i))
        button.pack(side="left")

    # Texte et boutons pour la sélection de la stratégie du joueur 2
    label_strat2 = tk.Label(root, text="Select the Strategy for Player 2 :")
    label_strat2.pack()
    strat2 = tk.StringVar()
    strat2.set("Strat 1")  # Stratégie par défaut
    strat2_buttons = tk.Frame(root)
    strat2_buttons.pack()
    for i in range(1, 8):
        button = tk.Radiobutton(strat2_buttons, text="Strat " +
                                str(i), variable=strat2, value="Strat " + str(i))
        button.pack(side="left")

    # texte et bouton pour la sélection du nombre d'itérations
    label_iter = tk.Label(root, text="Select the number of iterations :")
    label_iter.pack()
    iter = tk.StringVar()
    iter.set("10")  # 10 itérations par défaut
    iter_buttons = tk.Frame(root)
    iter_buttons.pack()
    for i in range(10, 31, 5):
        button = tk.Radiobutton(iter_buttons, text=str(i),
                                variable=iter, value=str(i))
        button.pack(side="left")
    

    
    # Bouton pour lancer la partie
    button = tk.Button(root, text="Let the GAME Begins", command=root.destroy)
    button.pack(pady=20)

    # Affichage de la fenêtre
    root.mainloop()
    

    # Récupération des valeurs sélectionnées
    st1 = strat1.get()
    st2 = strat2.get()
    itr = iter.get()


    # Affichage des valeurs sélectionnées
    print(st1)
    print(st2)
    print(itr)

    

    return st1, st2, itr




def main(str1, str2):

    #for arg in sys.argv:
    iterations = 100 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    #print ("Iterations: ")
    #print (iterations)

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
    #print(ligneObjectif)
    
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
    
    def is_between(x,y,z):
        return (x>=y and x<=z) or (x>=z and x<=y)
    
   
    #-------------------------------
    # Rapport de ce qui est trouve sut la carte
    #-------------------------------
    #print("lecture carte")
    #print("-------------------------------------------")
    #print("lignes", nbLignes)
    #print("colonnes", nbCols)
    #print("Trouvé ", nbPlayers, " joueurs avec ", int(nbWalls/2), " murs chacun" )
    #print ("Init states:", initStates)
    #print("-------------------------------------------")

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
    #print("Tous les objectifs joueur 0", allObjectifs[0])
    #print("Tous les objectifs joueur 1", allObjectifs[1])
    objectifs =  [allObjectifs[0][random.randint(cMin,cMax-3)], allObjectifs[1][random.randint(cMin,cMax-3)]]
    #print("Objectif joueur 0 choisi au hasard", objectifs[0])
    #print("Objectif joueur 1 choisi au hasard", objectifs[1])

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

        #print("IS OKAY PATH",path)
        
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
            #print("WALLL CURR",wall_curr)
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
        wall_curr=wallStates(allWalls)
        #print("WALLL CURR",wall_curr)
        muravance=1 if player==1 else 0
        random_loc = (posPlayers[1 - player][0],posPlayers[1 - player][1]+muravance)
        if legal_wall_position(random_loc, player, posPlayers,wall_curr):
            wall_curr.append(random_loc) 
            inc_pos =[(0,1),(0,-1),(1,0),(-1,0)] 
            random.shuffle(inc_pos)
            for w in inc_pos:
                random_loc_bis = (random_loc[0] + w[0],random_loc[1]+w[1])
                if legal_wall_position(random_loc_bis,player, posPlayers,wall_curr):
                    return(random_loc,random_loc_bis)
        
        return draw_random_wall_location(player, posPlayers)

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
        #print ("Chemin trouvé:", path)
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
            
        
        #print ("Chemin trouvé:", path_init)
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


    def choisir_les_murs(player,positions):
        legal_walls=[]
        for i in range(lMin,lMax):
            for j in range(cMin,cMax):
                voisins=[(0,1),(0,-1),(1,0),(-1,0)]
                for v in voisins:
                    murs_actuel=wallStates(allWalls)
                    if legal_wall_position((i,j), player, positions,murs_actuel):
                        murs_actuel.append((i,j))
                        if legal_wall_position((v[0]+i,v[1]+j), player, positions,murs_actuel):
                            if ((i,j),(i+v[0],j+v[1])) not in legal_walls and ((i+v[0],j+v[1]),(i,j)) not in legal_walls :
                                if(is_between(i,posPlayers[1-player][0],objectifs[1-player][0]) and is_between(j,posPlayers[1-player][1],objectifs[1-player][1])):
                                    legal_walls.append(((i,j),(i+v[0],j+v[1])))
        
        return legal_walls
    
    def calcul_path_A_star_Mininimax(player,positions,Wall_curr):
    
        g =np.ones((nbLignes,nbCols),dtype=bool)  # une matrice remplie par defaut a True  
        for w in Wall_curr:            # on met False quand murs
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
        p = ProblemeGrid2D(positions[player],objectifs[player],g,'manhattan')
        path_init = probleme.astar(p,verbose=False)
        #print ("Chemin trouvé:", path)

        for obj in allObjectifs[player]:
            p = ProblemeGrid2D(posPlayers[player],obj,g,'manhattan')
            path_dynamique = probleme.astar(p,verbose=False)
            if len(path_dynamique) < len(path_init):
                path_init = path_dynamique
                objectifs[player] = obj
        return path_init
    
    def decision_minimax(player,positions,Wall_curr,horizon):
        list_murs=choisir_les_murs(player,positions)
        meilleur_score=-1000
        meilleur_coup=draw_random_wall_location(player,posPlayers)
        for i in range(0,len(list_murs)):
            nouv_Wall_Curr=Wall_curr[:]
            nouv_Wall_Curr.append(list_murs[i][0])
            nouv_Wall_Curr.append(list_murs[i][1])
            score_eval=minimax_placer_murs(player,positions,nouv_Wall_Curr,horizon)
            if score_eval>meilleur_score:
                meilleur_coup=(list_murs[i][0],list_murs[i][1])

        return meilleur_coup

    def minimax_placer_murs(player,positions,Wall_curr,horizon):
        lng_joueur=len(calcul_path_A_star_Mininimax(player,posPlayers,Wall_curr))
        lng_adv=len(calcul_path_A_star_Mininimax(1 - player,posPlayers,Wall_curr))
        if horizon==1:
            return lng_adv-lng_joueur
        if horizon%2==1:
            list_murs=choisir_les_murs(player,positions)
            val=-1000
            for mur in list_murs:
                nouv_Wall_Curr=Wall_curr[:]
                nouv_Wall_Curr.append(mur[0])
                nouv_Wall_Curr.append(mur[1])
                val=max(val,minimax_placer_murs(player,positions,nouv_Wall_Curr,horizon-1))
            
            return val
        
        if horizon%2==0:
            list_murs=choisir_les_murs(1-player,positions)
            val=1000
            for mur in list_murs:
                nouv_Wall_Curr=Wall_curr[:]
                nouv_Wall_Curr.append(mur[0])
                nouv_Wall_Curr.append(mur[1])
                val=min(val,minimax_placer_murs(player,positions,nouv_Wall_Curr,horizon-1))
            
            return val




        
    
    def jouer_minimax(player, walls_used,horizon):
        """stratégie aléatoire avancée
        
        si le jouer est proche du cible on doit avancer et non pas constuire un mur aléatoirement
        """

        # calcul de la longeur du path pour les deux joeurs :
        wall_curr=wallStates(allWalls)
        position=posPlayers[player]
        lng_joueur=len(calcul_path_A_star_Mininimax(player,posPlayers,wall_curr))
        lng_adv=len(calcul_path_A_star_Mininimax(1 - player,posPlayers,wall_curr))
        if lng_joueur<2:
            return 100
        
        if lng_adv<2:
            return -100
        choix_du_jouer = 1 if lng_joueur < lng_adv else 0

        if choix_du_jouer==0:
            if walls_used[player]>=10 or position[0]<=4 or position[0]>=6:
                choix_du_jouer=1
            else:
                wall_to_remplir=walls_used[player]
                #wall_curr=wallStates(allWalls)
                ((x1,y1),(x2,y2)) = decision_minimax(player,posPlayers,wall_curr,horizon)
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
    

    ###################################################################################################################
    def decision_alpha_beta(player,positions,Wall_curr,horizon):
        list_murs=choisir_les_murs(player,positions)
        meilleur_score=-1000
        meilleur_coup=draw_random_wall_location(player,posPlayers)
        for i in range(0,len(list_murs)):
            nouv_Wall_Curr=Wall_curr[:]
            nouv_Wall_Curr.append(list_murs[i][0])
            nouv_Wall_Curr.append(list_murs[i][1])
            score_eval=alpha_beta_placer_murs(player,positions,nouv_Wall_Curr,horizon)
            if score_eval>meilleur_score:
                meilleur_coup=(list_murs[i][0],list_murs[i][1])

        return meilleur_coup

    def alpha_beta_placer_murs(player,positions,Wall_curr,horizon,alpha=-1000,beta=1000):
        lng_joueur=len(calcul_path_A_star_Mininimax(player,posPlayers,Wall_curr))
        lng_adv=len(calcul_path_A_star_Mininimax(1 - player,posPlayers,Wall_curr))
        if horizon==1:
            return lng_adv-lng_joueur
        
        if horizon%2==1:
            val=-1000
            list_murs=choisir_les_murs(player,positions)
            for mur in list_murs:
                nouv_Wall_Curr=Wall_curr[:]
                nouv_Wall_Curr.append(mur[0])
                nouv_Wall_Curr.append(mur[1])
                val=max(val,alpha_beta_placer_murs(player,positions,nouv_Wall_Curr,horizon-1,alpha,beta))
                if val >=beta:
                    break
                alpha=max(alpha,val)
            
            return val
        
        if horizon%2==0:
            val=1000
            list_murs=choisir_les_murs(1-player,positions)
            for mur in list_murs:
                nouv_Wall_Curr=Wall_curr[:]
                nouv_Wall_Curr.append(mur[0])
                nouv_Wall_Curr.append(mur[1])
                val=min(val,alpha_beta_placer_murs(player,positions,nouv_Wall_Curr,horizon-1,alpha,beta))
                if val <=alpha:
                    break
                beta=min(beta,val)
            
            return val




        
    
    def jouer_alpha_beta(player, walls_used,horizon):
        """stratégie aléatoire avancée
        
        si le jouer est proche du cible on doit avancer et non pas constuire un mur aléatoirement
        """

        # calcul de la longeur du path pour les deux joeurs :
        wall_curr=wallStates(allWalls)
        position=posPlayers[player]
        lng_joueur=len(calcul_path_A_star_Mininimax(player,posPlayers,wall_curr))
        lng_adv=len(calcul_path_A_star_Mininimax(1 - player,posPlayers,wall_curr))
        if lng_joueur<2:
            return 100
        
        if lng_adv<2:
            return -100
        choix_du_jouer = 1 if lng_joueur < lng_adv else 0

        if choix_du_jouer==0:
            if walls_used[player]>=10 or position[0]<=4 or position[0]>=6:
                choix_du_jouer=1
            else:
                wall_to_remplir=walls_used[player]
                #wall_curr=wallStates(allWalls)
                ((x1,y1),(x2,y2)) = decision_alpha_beta(player,posPlayers,wall_curr,horizon)
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
    
###############################################################################################################
    def choisir_les_murs_monaco(player,positions,murs_actuel):
        copy_murs_actuel=murs_actuel[:]
        legal_walls=[]
        for i in range(lMin,lMax):
            for j in range(cMin,cMax):
                voisins=[(0,1),(0,-1),(1,0),(-1,0)]
                for v in voisins:
                    if legal_wall_position((i,j), player, positions,murs_actuel[:]):
                        murs_actuel.append((i,j))
                        if legal_wall_position((v[0]+i,v[1]+j), player, positions,murs_actuel[:]):
                            if ((i,j),(i+v[0],j+v[1])) not in legal_walls and ((i+v[0],j+v[1]),(i,j)) not in legal_walls :
                                if(is_between(i,posPlayers[1-player][0],objectifs[1-player][0]) and is_between(j,posPlayers[1-player][1],objectifs[1-player][1])):
                                    legal_walls.append(((i,j),(i+v[0],j+v[1])))
                murs_actuel=copy_murs_actuel[:]
        
        return legal_walls
    def jouer_aleatoire_monaco(player, walls_used,Murs,positions,joueurs):
        """stratégie aléatoire ou les deux joeurs ont le choix entre avancer ou placer un mur aléatoirement 
        """
        choix_du_jouer=random.choice([0,1])

        if choix_du_jouer==0:
            if walls_used[player]>=10:
                choix_du_jouer=1
            else:
                #wall_to_remplir=walls_used[player]
                ((x1,y1),(x2,y2)) = draw_random_wall_location(player, posPlayers)
                #Murs[player][wall_to_remplir].set_rowcol(x1,y1)
                Murs.append((x1,y1))
                Murs.append((x2,y2))
                #Murs[player][wall_to_remplir+1].set_rowcol(x2,y2)
                walls_used[player]=walls_used[player]+2

        
        # on fait bouger le joueur 1 jusqu'à son but
        # en suivant le chemin trouve avec A* 
        if choix_du_jouer==1: #Il a choisi joueur
            path=calcul_path_A_star(player,positions)
            row,col = path[1]
            positions[player]=(row,col)
            #joueurs[player].set_rowcol(row,col)
            #print ("pos joueur",player,":",row,col)
            if (row,col) == objectifs[player]:
                return True, player
            
        return False, player
    

    def decision_monaco(player,positions,Wall_curr,walls_used,horizon):
        list_murs=choisir_les_murs_monaco(player,positions,Wall_curr)
        print(list_murs)
        meilleur_score=-1000
        meilleur_coup=draw_random_wall_location(player,posPlayers)
        for i in range(0,len(list_murs)):
            nouv_Wall_Curr=Wall_curr[:]
            nouv_Wall_Curr.append(list_murs[i][0])
            nouv_Wall_Curr.append(list_murs[i][1])
            score_eval=monaco_placer_murs(player,positions,nouv_Wall_Curr,walls_used,horizon,horizon)
            if score_eval>meilleur_score:
                meilleur_coup=(list_murs[i][0],list_murs[i][1])

        return meilleur_coup
    

    def monaco_placer_murs(player,positions,Wall_curr,walls_used,horizon,horizon_init,alpha=-1000,beta=1000):
        if horizon==1:
            print("ICI")
            if horizon_init%2==1:
                nbwin=0
                for k in range(10):
                    fin=False
                    Murs=Wall_curr[:]
                    pos=posPlayers[:]
                    joueurs=players[:]
                    while(not fin):
                        fin,gagnat=jouer_aleatoire_monaco(player,walls_used,Murs,pos,joueurs)
                        if not fin:
                            fin,gagnat=jouer_aleatoire_monaco(1-player,walls_used,Murs,pos,joueurs)
                    if gagnat==player:
                        nbwin=nbwin+1
                
                return nbwin/10
            
            if horizon_init%2==0:
                nbwin=0
                for k in range(10):
                    fin=False
                    Murs=Wall_curr[:]
                    pos=posPlayers[:]
                    joueurs=players[:]
                    while(not fin):
                        fin,gagnat=jouer_aleatoire_monaco(1-player,walls_used,Murs,pos,joueurs)
                        if not fin:
                            fin,gagnat=jouer_aleatoire_monaco(player,walls_used,Murs,pos,joueurs)
                    if gagnat==player:
                        nbwin=nbwin+1
                
                return nbwin/10

        
        if horizon%2==1:
            val=-1000
            list_murs=choisir_les_murs_monaco(player,positions,Wall_curr[:])
            for mur in list_murs:
                nouv_Wall_Curr=Wall_curr[:]
                nouv_Wall_Curr.append(mur[0])
                nouv_Wall_Curr.append(mur[1])
                val=max(val,monaco_placer_murs(player,positions,nouv_Wall_Curr,horizon-1,horizon_init,alpha,beta))
                if val >=beta:
                    break
                alpha=max(alpha,val)
            
            return val
        
        if horizon%2==0:
            val=1000
            list_murs=choisir_les_murs_monaco(1-player,positions,Wall_curr[:])
            for mur in list_murs:
                nouv_Wall_Curr=Wall_curr[:]
                nouv_Wall_Curr.append(mur[0])
                nouv_Wall_Curr.append(mur[1])
                val=min(val,monaco_placer_murs(player,positions,nouv_Wall_Curr,horizon-1,horizon_init,alpha,beta))
                if val <=alpha:
                    break
                beta=min(beta,val)
            
            return val
    
    def jouer_monaco(player, walls_used,horizon):
        """stratégie aléatoire avancée
        
        si le jouer est proche du cible on doit avancer et non pas constuire un mur aléatoirement
        """

        # calcul de la longeur du path pour les deux joeurs :
        wall_curr=wallStates(allWalls)
        position=posPlayers[player]
        lng_joueur=len(calcul_path_A_star_Mininimax(player,posPlayers,wall_curr))
        lng_adv=len(calcul_path_A_star_Mininimax(1 - player,posPlayers,wall_curr))
        if lng_joueur<2:
            return 100
        
        if lng_adv<2:
            return -100
        choix_du_jouer = 1 if lng_joueur < lng_adv else 0

        if choix_du_jouer==0:
            if walls_used[player]>=10 or position[0]<=4 or position[0]>=6:
                choix_du_jouer=1
            else:
                wall_to_remplir=walls_used[player]
                #wall_curr=wallStates(allWalls)
                ((x1,y1),(x2,y2)) = decision_monaco(player,posPlayers,wall_curr,walls_used,horizon)
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

            
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    def perform(strategy):
        if strategy == 'Strat 1':
            return jouer_aleatoire(player, walls_used)
        elif strategy == 'Strat 2':
            return jouer_aleatoire_avance(player, walls_used)
        elif strategy == 'Strat 3':
            return jouer_objectif_proche(player, walls_used)
        elif strategy == 'Strat 4':
            return jouer_placer_mur_proche(player, walls_used)
        elif strategy == 'Strat 5':
            return jouer_minimax(player, walls_used, 3)
        elif strategy == 'Strat 6':
            return jouer_alpha_beta(player, walls_used,5)
        else:
            return jouer_monaco(player, walls_used,1)
        
        
            
    posPlayers = initStates

    #print(iterations)


    walls_used=[0,0]
    for i in range(iterations):

        player=2
        if i%2==0:
            player=0
        else:
            player=1

        # print("Le joueur actuel :",player)
        end,gagnat = perform(str1) if player%2==0 else perform(str2)
        
        if end:
            return gagnat
        
        # mise à jour du pleateau de jeu
        game.mainiteration()
        # print(walls_used)
    
    pygame.quit()
    
    
    
    
    #-------------------------------
    
        
    
    
from collections import Counter

if __name__ == '__main__':

    # appeler la fonction welcome_frame() pour afficher la fenetre de bienvenue
    # et que l'utilisateur choisisse le nombre de parties à jouer
    # ainsi que les stratégies des joueurs
    str1, str2, itr = welcome_frame()

    gagnat = []
    alea=0
    for i in range(0,int(itr)):
         gagnat.append(main(str1,str2))
    count = Counter(gagnat)
    most_common_element = count.most_common(1)[0][0]
    cpt=count.most_common(1)[0][1]
    print("Le gagnant de partie est ",most_common_element)
    print("Il a gagné ",cpt," jeu.")
    
    # gagnat = []
    # alea=1
    # for i in range(0,50):
    #      gagnat.append(main())
    # count = Counter(gagnat)
    # most_common_element = count.most_common(1)[0][0]
    # cpt=count.most_common(1)[0][1]
    # print("Le gagnant de partie est ",most_common_element)
    # print("Il a gagné ",cpt," jeu.")

    # alea=0
    # main()
    


    
    
    


