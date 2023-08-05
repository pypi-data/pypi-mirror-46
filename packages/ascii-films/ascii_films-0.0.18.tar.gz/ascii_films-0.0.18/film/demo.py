#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
#
#  exemple.py
#
#  Copyright 2019 Robert Sebille <robert@sebille.name>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import os.path as p
import webbrowser as wb

if __name__ == "__main__":
    from film import Film
else:
    from film.film import Film

chemin = p.dirname(p.abspath(__file__)) + "/"


def demo():

    # wb.open("https://upload.wikimedia.org/wikipedia/commons/7/73/Roflcopter.gif")

    ################
    # Présentation #
    ################
    # l'instance f de Film est ici utilitaire pour les goto, print_*, etc.
    f = Film()

    # on efface l'écran. Méthode de classe, car quand on efface l'écran,
    # c'est pour tous les objets films()
    Film.clearsc()

    # goto: place le curseur à x, y pour impression
    f.goto(29, 8)

    # Imprime un message à x, y, message, delai=2, revers=True
    # en inversé, couleur et background, si revers=True, sinon normal
    f.print_message(20, 6, "Les cinémas ellibeS treboR présentent")
    # retourne la version de la classe
    f.print_message(30, 8, "Version " + Film.version(), 2, False)

    f.print_message(23, 6, "Une soirée exceptionnelle !")
    f.print_message(18, 10, "Des actualités sportives !", 2, False)
    f.print_message(35, 4, "Une magnifique série Superflix !", 2, False)
    f.print_message(30, 10, "Des grands films !", 2, False)
    # Méthode de classe qui évite l'importation de la méthode sleep
    # du module time
    Film.delay(1)

    ############################
    # Les actualités sportives #
    ############################
    f.print_message(22, 6, "Et d'abord les actualités sportives")
    f.print_message(22, 6, "Avec notre grand champion Cava Zeter",
                    2, False)
    Film.delay(1)

    # Ah, un premier film et son dictionnaire de sous-titres
    # les tuple clés sont les range de n° de frame où le sous-titre
    # doit s'afficher
    d0 = {
        (3, 6):   "Han !",
        (10, 13): "Gnaaa !",
        (18, 21): "Pfiouu !",
        (25, 28): "Victoire !"
        }
    f0 = Film("Le lancer du smart-o", d0)
    # C'est un film "statique", les frames ne se déplacent pas
    # Les films suivants, les frames se déplaceront. par défaut,
    # le deplacement = 1
    f0.deplacement = 0
    f0.frame = chemin + "frame/lancer_marteau"
    # Très utile: ceci m'indique le nombre de frames du fichier !
    # print("nb frame f0 : ", f0.nb_frames_per_file)
    # input("Pressez une touche pour continuer ...")

    # Les coordonnées par defaut des sous-titres (20, 15) sont un peu trop
    # basses. on les relève à y=11
    f0.sous_titre_xy = (20, 11)
    # Projection d'un film: (nb_frames=0, x=2, y=2, trace=0, delai=0.1)
    # Voyez la documentation de la classe.
    f0.projection(29, 22, delai=0.15)
    Film.delay(1)
    Film.clearsc()

    f.print_message(23, 6, "Superbe ! Extraordinaire !", 2, False)
    f.print_message(23, 6, "Revoyons cela au ralenti ... ", 2, False)
    Film.delay(1)

    f0.projection(29, 22, delai=0.3)
    Film.delay(1)
    Film.clearsc()
    f.print_message(20, 6, "Epoustouflant lancer du smart-o de Cava Zeter !",
                    2.5, False)

    ##############
    # Les séries #
    ##############
    f.print_message(15, 6, "Et maintenant place à notre grande série \
SuperFlix")
    f.print_message(30, 6, "Les ROFL !!!")
    Film.delay(1)

    f.print_message(20, 6, "1er épisode : Le ROFLCOPTER historique")
    Film.delay(1)
    # Dictionnaire dans les frames du vol en déplacement > 10)
    d1 = {
        (12, 20): "Je vole, je colle",
        (25, 33): "je caracolle",
        (38, 46): "je cabricolle",
        (51, 59): "et je rigole",
        (65, 82): "et glou, et glou, ... Ha ha ha !"
    }
    f1 = Film("Le ROFLCOPTER historique", d1)
    f1.frame = chemin + "frame/roflcopter"
    # Vol stationnaire
    f1.deplacement = 0
    f1.projection(10, 2, 4)
    # vol en déplacement de 1
    f1.deplacement = 1
    ###
    f1.projection(84, 2, 4)
    f1.deplacement = 0
    f1.projection(10, 84, 4)
    Film.delay(1)
    Film.clearsc()
    Film.delay(1)

    f.print_message(20, 6, "2ème épisode : Le ROFLPLANE et la Postale")
    Film.delay(1)
    # Dictionnaire dans les frames du vol en déplacement > 10)
    d1 = {
        (12, 20): "T'as pas vu ?",
        (25, 33): "Non, quoi ?",
        (38, 56): "Rien, j'ai cru voir un mouton voler",
        (60, 70): "avec un drôle de zigue",
    }
    f1 = Film("Le ROFLPLANE et la Postale", d1)
    f1.frame = chemin + "frame/roflplane"
    # Vol stationnaire
    f1.deplacement = 0
    f1.projection(10, 2)
    # vol en déplacement de 1
    f1.deplacement = 1
    f1.projection(84, 2)
    f1.deplacement = 0
    f1.projection(10, 84)
    Film.delay(1)
    Film.clearsc()
    Film.delay(1)

    f.print_message(15, 6, "3ème épisode : La ROFLFLYINGMOTO, \
on ne vit deux fois")
    Film.delay(1)
    # Dictionnaire dans les frames du vol en déplacement > 10)
    d1 = {
        (15, 25): "Ouf ti !",
        (32, 42): "Ca tape la vitesse !",
        (49, 59): "Bon, je freine.",
    }
    f1 = Film("La ROFLFLYINGMOTO, on ne vit deux fois.", d1)
    f1.frame = chemin + "frame/roflflyingmoto"
    # Vol stationnaire
    f1.deplacement = 0
    f1.projection(10, 2, 4)
    # vol en déplacement de 1
    f1.deplacement = 1
    # delai à 0.05 = impression de vitesse
    f1.projection(84, 2, 4, delai=0.025)
    f1.deplacement = 0
    # on redefinit les sous-titres
    f1.dict_sous_titres = {(2, 8): " Ouf, j'ai eu chaud ! "}
    f1.projection(10, 84, 4)
    Film.delay(1)
    Film.clearsc()
    Film.delay(1)

    f.print_message(10, 6, "4ème épisode : Le ROFLFLYINGCAT ou le retour \
de l'esprit frappeur")
    Film.delay(1)
    # Dictionnaire dans les frames du vol en déplacement > 10)
    d1 = {
        (15, 25): "c'est le p'tit bout",
        (32, 42): "d'la queue",
        (49, 59): "du chat",
        (66, 76): "qui vous électrise.",
    }

    f1 = Film("Le ROFLFLYINGCAT ou le retour de l'esprit frappeur.", d1)
    f1.frame = chemin + "frame/roflflyingcat"
    # Vol stationnaire
    f1.deplacement = 0
    f1.projection(10, 2)
    # vol en déplacement de 1
    f1.deplacement = 1
    f1.projection(85, 2, 4, 1)
    f1.deplacement = 0
    f1.projection(10, 85)
    Film.delay(1)
    Film.clearsc()
    f.print_message(20, 6, "Ah les frères Jacques et la Queue du chat ;-)",
                    rev=False)
    f.print_message(15, 6, "Voilà qui cloture notre série de séries, \
ah ah !", rev=False)
    f.print_message(25, 6, "Bon, soit !", 1, False)
    Film.delay(1)

    ####################
    # Les grands films #
    ####################
    # On crée 3 nouveaux films (f2, 3, 4), avec leur titre (non requis),
    # leur diction de sous-titre(non-resuis) et leur(s) fichier(s) de freme(s)
    # requis avant de jouer le film
    d2 = {
        (5, 10):  "Bonjour",
        (20, 27): "Quelle belle promenade !",
        (34, 41): "Et quel temps agréable.",
        (48, 55): "Allez, au revoir",
        }

    f2 = Film("La promenade tranquille ...", d2)
    f2.frames = chemin + "frames/"
    # f2 est un film très tranquille, pour pimenter un peu, on va mettre
    # les sous-titres en impression reverse
    f2.sous_titres_reverse = True
    # De plus les sous-titres par défaut sont trop haut, on les baisse
    f2.sous_titre_xy = (20, 18)

    d3 = {
        (5, 10):  "Je t'aurai, brigand !",
        (15, 20): "Essaie toujours, sacripant !",
        (25, 30): "Tu ne t'en sortiras pas, fripouille !",
        (35, 40): "Numérotte tes abattis, misérable !"
        }

    f3 = Film("La poursuite impitoyable", d3)
    f3.frame = chemin + "frame/poursuiteci"
    f3.sous_titre_xy = 20, 13

    f4 = Film("La poursuite effroyable")
    f4.frame = chemin + "frame/poursuiteic"
    f4.sous_titre_xy = 20, 13

    Film.clearsc()

    f.print_message(20, 6, "Et maintenant, nos grands films !")
    f.print_message(23, 6, "Et sur écran géant, svp !")
    Film.clearsc()
    Film.delay(1)
    # get_titre property, bon, faut-il l'expliquer? ;)
    f.print_message(25, 6, "1. " + f2.titre)

    # On monte l'écran géant ! ;)
    f2.dessine_ecran(2, 1, 79, 20)
    # lance le film f2. 66 frames à jouer, démarrer le film en 2, 2
    # 0 blanc de "trace", delai de 0.2 secondes par frame
    # Rappel: deplacement = 1 par défaut
    f2.projection(64, 3, 4, 0, 0.2)
    f.print_message(27, 6, "Sniff ! Que c'était beau !", rev=False)
    Film.clearsc()
    f.print_message(20, 6, "Et quelle subtile émotion !", rev=False)
    Film.clearsc()
    Film.delay(1)

    f3.print_message(25, 6, "2. " + f3.titre)
    Film.delay(1)
    f3.dessine_ecran(2, 1, 79, 15)
    f3.projection(44, 3, 4, 0, 0.2)
    f3.print_message(13, 6, "Quelle suspense époustouflant !", rev=False)
    f3.print_message(13, 6, "Rembobinons ?", 1, rev=False)
    f3.print_message(13, 6, "Rembobinons !", 1, rev=False)
    # Place le sens du film en arrière
    f3.reverse = True
    f3.dessine_ecran(2, 1, 79, 15)
    # on a mis un débit par frame plus rapide pour le rembobinage
    f3.projection(42, 45, 4, 0, 0.05)
    Film.delay(1)
    Film.clearsc()
    f3.print_message(13, 6, "Et rejouons ce splendide film ! ", rev=False)
    # on replace le sens du film en avant
    f3.reverse = False
    f3.dessine_ecran(2, 1, 79, 15)
    f3.projection(44, 3, 4, 0, 0.2)
    f3.print_message(10, 6, "Quelle film ! On ne s'en lasse pas !", rev=False)
    f3.print_message(10, 6, "Mais ce n'est pas tout, voyons la suite",
                     rev=False)

    Film.clearsc()
    # Finalement, on change de titre
    f4.titre = "La revanche des indiens"
    # On ajoute les sous-titres par après, on peut
    f4.dict_sous_titres = {
        (5, 10):  "Ha ha, on ne dit plus rien, gredin !",
        (15, 20): "C'est ce que tu crois, petit fripon !",
        (25, 30): "Je te tiens cette fois, chenapan !",
        (35, 40): "Compte là-dessus, coquin !"
        }
    f4.print_message(25, 6, "3. " + f4.titre)
    f4.print_message(25, 6, "Ha ha !", rev=False)
    f4.dessine_ecran(2, 1, 79, 15)
    f4.projection(44, 3, 4, 0, 0.2)
    Film.delay(1)

    Film.clearsc()
    f4.print_message(21, 6, "Voilà, cette formidable soirée est finie !")
    f4.print_message(24, 6, "A bientôt, et à vous de jouer !")

    Film.clearsc()
    f.goto(0, 0)
    print("Le code de la demo est disponible ici:")
    print("https://framagit.org/zenjo/film/blob/master/film/demo.py")
    rep = ""
    while rep not in ["o", "n"]:
        rep = input("Souhaitez-vous l'ouvrir dans votre navigateur o/n ?")
        rep = rep.lower()
    Film.clearsc()
    if rep == "o":
        wb.open("https://framagit.org/zenjo/film/blob/master/film/demo.py")
        f.print_message(0, 0, "Voilà, c'est fait.", rev=False)
    else:
        f.print_message(0, 0, "Ok, une prochaine fois peut-être.", rev=False)
    f.print_message(0, 0, "Voici l'aide de la classe Film; pressez \"q\" pour\
 en sortir.", rev=False)
    help(Film)
    print("\n\n\n")


if __name__ == '__main__':
    demo()
    pass
