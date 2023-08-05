#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
#
#  class Film.py
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


from time import sleep
from os import listdir


class Film:
    """Cette classe fournit des outils pour afficher des petits films
    à partir de frames en ascii.

    Les frames peuvent être dans un seul fichier, avec un séparateur ou
    dans plusieurs fichiers qui seront lus d'un répertoire à préciser,
    et dans l'ordre alphanumérique croissant.

    Pour démarrer, essayez ceci, ci dessous ?

    .. code-block::

        from film.film import Film
        Film.demo()

    .. seealso::
        Dépot: https:///framagit.org/zenjo/film/tree/master
    """

    _version = "0.0.18"

    def __init__(self, titre="", dict_sous_titres={}):
        """
        Constructeur

        self._ecran: bascule pour l'effacement de l'écran entre les
        méthodes projection et dessine_ecran
        """
        self._titre = str(titre)
        self._frames = []
        self._reverse = False
        self._affiche_titre = True
        self._affiche_ctrl_c = False
        self._ctrl_c_xy = (0, 15)
        self._titre_x = 4
        self._titre_xy = (self.titre_x, 2)
        self._dict_sous_titres = dict_sous_titres
        self._sous_titre_xy = (20, 15)
        self._sous_titres_largeur = 40
        self._sous_titres_reverse = False
        self._deplacement = 1
        self._affiche_no_frame = False
        self._no_frame_xy = (0, 0)
        self._nb_frames = 0
        self._nb_frames_per_file = 0
        self._ecran = False

    def __str__(self):
        """Retoune la chaîne "Film : Titre du film" """
        return str("Film : " + self.titre)

    # Private
    def __ccls(cls):  # clear the screen
        return "\033[2J"
    __ccls = classmethod(__ccls)

    def __ccxy2(self, x, y):  # position cursor at x across, y down
        return "\033["+str(y)+";"+str(x)+"f"

    def __ccxy1(self, coords):  # position cursor at coords[0] across, ...
        print("\033["+str(coords[1])+";"+str(coords[0])+"f", sep="", end="")

    def __csrv(self):  # print reverse
        return "\033[7m"

    def __csrs(self):  # print, reset all
        return "\033[0m"

    # Public
    # class methods
    def version(cls):
        """Retourne la version de la classe"""
        return cls._version
    version = classmethod(version)

    def delay(cls, secondes):
        """Evite l'importation de la méthode sleep du module time"""
        sleep(secondes)
    delay = classmethod(delay)

    def clearsc(cls):
        """Efface l'écran."""
        print(cls.__ccls())
    clearsc = classmethod(clearsc)

    def demo(cls):
        """Lance une demo amusante de la classe"""
        from film.demo import demo
        demo()
    demo = classmethod(demo)

    # property
    def get_titre(self):
        return self._titre

    def set_titre(self, titre):
        self._titre = str(titre)

    titre = property(get_titre, set_titre, '',
                     """
    Retourne, modifie ou crée le titre du film. Défaut = ''""")

    def set_frame(self, fichier, sep="#"):
        self._nb_frames_per_file = 0
        with open(fichier) as c:
            liste = c.readlines()
        s = "".join(liste)
        liste = s.split(sep)
        for l in liste:
            self._frames.append(l.split("\n"))
            self._nb_frames_per_file += 1
            self._nb_frames += 1

    def del_frame(self):
        self._frames = []
        self._affiche_no_frame = False
        self._nb_frames = 0
        self._nb_frames_per_file = 0

    frame = property('', set_frame, del_frame,
                     """
    Lit ou ajoute des frames à partir d'un seul fichier. Ces frames sont
    séparées par un séparateur, par défaut #

    del frame détruit toutes les frames du film
    """)

    def set_frames(self, repertoire):
        frms = []
        for fichier in listdir(repertoire):
            with (open(repertoire + '/' + fichier)) as f:
                frms.append(f.read())
                self._nb_frames += 1
        for f in frms:
            self._frames.append(f.split("\n"))
        self._nb_frames_per_file = 1

    def del_frames(self):
        self.del_frame()

    frames = property('', set_frames, del_frames,
                      """
    Lit ou ajoute des frames à partir de fichiers dans un répertoire.
    Chaque frame est dans un fichier propre. Les fichiers sont lus dans
    le répertoire dans le sens alphnumérique croissant de leurs noms.")

    del frames détruit toutes les frames du film
    """)

    def get_nb_frames(self):
        return self._nb_frames

    nb_frames = property(get_nb_frames, '', '',
                         """
    Retourne

        - 0 si aucune frame n'est définie
        - le nombre de frames du film

    .. note::
        sera egal à nb_frames_per_file dans le cas d'un fichier unique
        """)

    def get_nb_frames_per_file(self):
        return self._nb_frames_per_file

    nb_frames_per_file = property(get_nb_frames_per_file, '', '',
                                  """
    Retourne

        - 0 si aucune frame n'est définie
        - 1 si les dernières frames chargées le sont à partir d'1 fichier
          par frame (cas de frames)
        - le nombre de frames dans le dernier fichier chargé si il s'agit
          d'un fichier unique

        """)

    def get_titre_x(self):
        return self._titre_x

    def set_titre_x(self, titre_x):
        self._titre_x = titre_x
        self._titre_xy[0] = titre_x

    titre_x = property(get_titre_x, set_titre_x, '',
                       """
    Retourne ou fixe la coordonnée x d'affichage du titre. Defaut=(4)

    Déprécié: utilisez titre_xy = (x, y) à la place

    .. note::
        Si vous utilisez titre_x, la valeur x de titre_xy sera automatiquement
        adaptée
    """)

    def get_titre_xy(self):
        return self._titre_xy

    def set_titre_xy(self, titre_xy):

        self._titre_xy = titre_xy
        self._titre_x = titre_xy[0]

    titre_xy = property(get_titre_xy, set_titre_xy, '',
                        """
    Retourne ou fixe les coordonnées x, y d'affichage du titre.
    Defaut=(4,2)

    obj.titre_xy = (x, y) # tuple

    .. note::
        obj.titre_x sera adapté à la valeur x de obj.titre_xy
    """)

    def get_dict_sous_titres(self):
        return self._dict_sous_titres

    def set_dict_sous_titres(self, dict_sous_titres):
        self._dict_sous_titres = dict_sous_titres

    dict_sous_titres = property(get_dict_sous_titres, set_dict_sous_titres, '',
                                """
    Retourne, modifie ou crée le dictionnaire des sous-titres

    Ce dictionnaire est de la forme: {(a, b): "sous-titre"}
    ou a = n° de la frame où l'affichage de "sous-titre" démarre et
    b = n° - 1 de la frame où s'arrête l'affichage de "sous-titre"
    """)

    def get_sous_titre_xy(self):
        return self._sous_titre_xy

    def set_sous_titre_xy(self, sous_titre_x_offset_y):
        self._sous_titre_xy = sous_titre_x_offset_y

    sous_titre_xy = property(get_sous_titre_xy, set_sous_titre_xy, '',
                             """
    Retourne ou fixe les coordonnées (x, y) de la zone de sous-titres
    Defaut=(20,15)

    obj.sous_titre_xy = (x, y) # tuple

    La zone de sous-titres débute à la coordonnée x de la largeur
    fixée (par défaut 40) par l'attribut sous_titres_largeur. Les sous-titres
    sont centrés dans cette zone.

    .. note::
        Pour mieux voir et comprendre ceci, mettez le paramètre
        sous_titres_reverse à True, le temps éventuellement de tester
        la projection de votre film.

    .. code-block::

        largeur zone sous-titre:  -> +-------- 20 --------+
                    sous_titre_xy -> |     Sous-titre     |
        le sous-titre est centré dans la zone de sous-titres

    """)

    def get_sous_titres_largeur(self):
        return self._sous_titres_largeur

    def set_sous_titres_largeur(self, sous_titres_largeur):
        self._sous_titres_largeur = sous_titres_largeur

    sous_titres_largeur = property(get_sous_titres_largeur,
                                   set_sous_titres_largeur, '',
                                   """
    Retourne ou fixe la largeur de la zone des sous-titres. Défaut = 40""")

    def get_sous_titres_reverse(self):
        return self._sous_titres_reverse

    def set_sous_titres_reverse(self, sous_titres_reverse):
        self._sous_titres_reverse = sous_titres_reverse

    sous_titres_reverse = property(get_sous_titres_reverse,
                                   set_sous_titres_reverse, '',
                                   """
    Retourne ou fixe l'affichage des sous-titres à reverse ou non.
    (booléen) Défaut = False""")

    def get_deplacement(self):
        return self._deplacement

    def set_deplacement(self, deplacement):
        self._deplacement = deplacement

    deplacement = property(get_deplacement, set_deplacement, '',
                           """
    Retourne ou fixe la valeur du déplacement entre 2 frames successives
    Défaut = 1""")

    def get_reverse(self):
        return self._reverse

    def set_reverse(self, direction):
        self._reverse = direction

    reverse = property(get_reverse, set_reverse, '',
                       """
    Retourne ou fixe le sens du film en avant ou en arrière (booléen)
    Défaut = False""")

    def get_affiche_titre(self):
        return self._affiche_titre

    def set_affiche_titre(self, affiche_titre):
        self._affiche_titre = affiche_titre

    affiche_titre = property(get_affiche_titre, set_affiche_titre, '',
                             """
    Retourne ou décide si il faut afficher le titre (booléen)
    Défaut = True""")

    def get_affiche_ctrl_c(self):
        return self._affiche_ctrl_c

    def set_affiche_ctrl_c(self, affiche_ctrl_c):
        self._affiche_ctrl_c = affiche_ctrl_c

    affiche_ctrl_c = property(get_affiche_ctrl_c, set_affiche_ctrl_c, '',
                              """
    Retourne ou décide si il faut afficher une mention CTRL + C (booléen)
    Défaut = False""")

    def get_ctrl_c_xy(self):
        return self._ctrl_c_xy

    def set_ctrl_c_xy(self, ctrl_c_xy):
        self._ctrl_c_xy = ctrl_c_xy

    ctrl_c_xy = property(get_ctrl_c_xy, set_ctrl_c_xy, '',
                         """
    Retourne ou fixe les coordonnées de l'affichage du CTRL + C, si
    affiche_ctrl_c = True. Défaut = (0, 15)""")

    def get_affiche_no_frame(self):
        return self._affiche_no_frame

    def set_affiche_no_frame(self, affiche_no_frame):
        self._affiche_no_frame = affiche_no_frame

    affiche_no_frame = property(get_affiche_no_frame, set_affiche_no_frame, '',
                                """
    Retourne ou décide si il faut afficher le n° de la frame en cours (booléen)
    Défaut = False

    .. note::
        Pratique en conjonction avec un long délai dans la méthode projection,
        pour régler finement la projection d'un ou de film(s), de sous-titres,
        ...

    Exemple:

    .. code-block::

        obj.affiche_no_frame = True
        obj.projection(delai = 0.5)
    """)

    def get_no_frame_xy(self):
        return self._no_frame_xy

    def set_no_frame_xy(self, no_frame_xy):
        self._no_frame_xy = no_frame_xy

    no_frame_xy = property(get_no_frame_xy, set_no_frame_xy, '',
                           """
    Retourne ou fixe les coordonnées de l'affichage n° de frame en cours, si
    affiche_no_frame = True. Défaut = (0, 0)""")

    # public methods
    def projection(self, nb_frames2run=0, x=2, y=4, trace=0, delai=0.1):
        """Lance l'instance film en lisant les frames.

        - nb_frames2run: nombre de frames à exécuter. 0 = infini
        - x, y: les coordonnées haut gauche de départ du film
        - trace nombre de blancs à ajouter à la frame suivant le sens du film.
          A gauche si self.reverse = False, à droite si self.reverse = True.
          Ce paramètre sert à effacer d'éventuelles traces laissées par une
          frame pas trop bien :) formatée.
        - delai: la durée en seconde de chaque frame

        .. note:: Le nombre de frames réellement exécutées sera le premier
            multiple de nb_frames au dessus de nb_frames2run - 1. nb_frames
            est égal au nombre de frames du film. Ainsi, pour un nb_frames2run
            = 17 et un nb_frames = 4, le nombre de frames exécutées sera 20 - 1
            = 20 (puisque le numérotage démarre à 0). Utilisez
            affiche_no_frame = True pour mieux visualiser cela.

        .. warning:: Si self.reverse = True, le film peut avoir des effets de
                     bord non désiré quand x < 0. Vous pouvez régler cela via
                     l'appel de la méthode.
        """

        if not self._ecran:
            self.clearsc()
        else:
            self._ecran = False
        if self.affiche_titre:
            self.__ccxy1(self.titre_xy)
            print(self.get_titre())
        if self.reverse:
            after = " " * trace
            before = ""
        else:
            after = ""
            before = " " * trace

        no_frame = 0
        while no_frame < nb_frames2run or nb_frames2run == 0:
            try:
                for f in self._frames:
                    # affichage du n° de la frame
                    if self.affiche_no_frame and self.nb_frames != 0:
                        self.__ccxy1(self.no_frame_xy)
                        print("frame " + str(no_frame % self.nb_frames) + " "
                              + str(no_frame) + " " + str(nb_frames2run))
                    # affichage de la frame
                    for l in range(len(f)):
                        self.goto(x, y + l)
                        print(before + f[l] + after)
                    # Traitement des sous-titres
                    self.__ccxy1(self._sous_titre_xy)
                    print(" "*40)
                    for k, v in self._dict_sous_titres.items():
                        if no_frame in range(int(k[0]), int(k[1])):
                            self.__ccxy1(self._sous_titre_xy)
                            if self.sous_titres_reverse:
                                self.print_reverse(
                                    v.center(self.
                                             sous_titres_largeur, " "))
                            else:
                                print(v.center(self.sous_titres_largeur, " "))
                    # affichage éventuel du CTRL+C
                    if self.affiche_ctrl_c:
                        self.__ccxy1(self.ctrl_c_xy)
                        print(" CTRL + C to stop.")
                    sleep(delai)
                    if self.reverse:
                        x -= self.deplacement
                    else:
                        x += self.deplacement
                    # delta no_frame
                    no_frame += 1
            except KeyboardInterrupt:
                print("\nReçu CTRL + C")
                print("Bye !")
                exit(0)

    def goto(self, x, y):
        """Amène le curseur en x, y pour impression (print)"""
        print(self.__ccxy2(x, y), sep="", end="")

    def print_reverse(self, message):
        """Inverse couleur et background pour l'impression d'un message"""
        print(self.__csrv() + message + self.__csrs())

    def print_message(self, x, y, message, delai=2, rev=True):
        """
        Affiche un message en reverse à x,y pour delai seconde (2 par défaut)
        """
        self.goto(x, y)
        self.print_reverse(" " + message + " ") if rev else print(message)
        self.delay(delai)
        self.goto(x, y)
        print(" "*(len(message)+2))

    def dessine_ecran(self, x0, y0, x1, y1, g="j", h="+", d="l", b="=",
                      c1="\\", c2="/"):
        """
        Dessine un écran, coin haut gauche = x0, y0, bas droit = x1, y1.
        g = bord gauche, h = haut, d = droit, b = bas, c1 = coin 1, c2 =coin 2

        .. code-block::

            (x0,y0) ->  c1hhhhhhc2 <- (x1,y0)  obj.dessine-ecran(1, 1, 10, 5)
                        g        d             retournera   \\++++++++/
                        g        d             par défaut   j        l
                        g        d                          j        l
                        g        d                          j        l
            (x0,y1) ->  c2bbbbbbc1 <- (x1,y1)               /========\\
        """
        self.clearsc()
        self._ecran = True
        self.goto(x0, y0)
        print(c1, sep="", end="")
        print(h*(x1-x0-1), sep="", end="")
        print(c2)
        for i in range((y0+1), (y1)):
            self.goto(x0, i)
            print(g, sep="", end="")
            self.goto(x1, i)
            print(d)
        self.goto(x0, y1)
        print(c2, sep="", end="")
        print(b*(x1-x0-1), sep="", end="")
        print(c1)
