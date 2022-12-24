#! /usr/bin/env python3
"""
All methods to use about a road in the game
"""
import curses
import time
from random import randint
from itertools import combinations
from geometry import Point
from methodsCurses import do_move_road, is_coordinate_valid_after_movment_road


def build_road_between_rooms(rooms, win, liste_points_pad):
    """
    build a road between room1 and room2
    """

    liste_couple_rooms = list(combinations(rooms, 2))
    for ch_mum, couple_room in enumerate(liste_couple_rooms):
        liste_points_chemin = []
        liste_points_deja_visites = []
        absc = 0
        ordo = 0
        porte_room1 = couple_room[0].liste_portes[randint(0, len(couple_room[0].liste_portes)-1)]
        porte_room2 = couple_room[1].liste_portes[randint(0, len(couple_room[1].liste_portes)-1)]
        point = porte_room1
        time_max_building_roads = time.time() + 5
        with open("logs/fichier_ch_num("+str(ch_mum)+").log", "w") as fichier_log:
            while not point.is_in_voisinage(porte_room2):

                if time.time() > time_max_building_roads:
                    return liste_points_pad
                liste_mouvement = [(curses.KEY_LEFT, Point(point.ordo, point.absc-1)),\
                    (curses.KEY_RIGHT, Point(point.ordo, point.absc+1)), \
                    (curses.KEY_UP, Point(point.ordo-1, point.absc)),\
                        (curses.KEY_DOWN, Point(point.ordo+1, point.absc))]
                liste_mouvemement_possibles = []

                for movement in liste_mouvement:
                    if is_coordinate_valid_after_movment_road(movement[1].ordo,\
                        movement[1].absc, rooms, win, liste_points_deja_visites, liste_points_pad):
                        liste_mouvemement_possibles.append(movement)
                distance_min = 100000
                index_final = 0
                for index, movement in enumerate(liste_mouvemement_possibles):
                    if porte_room2.distance_to(movement[1]) <= distance_min:
                        index_final = index
                        distance_min = porte_room2.distance_to(movement[1])
                try:
                    mouvement_optimal = liste_mouvemement_possibles[index_final]
                except IndexError as message:
                    fichier_log.write("\n EXCEPTION ! \n"+str(message)+"\n\n")
                    break
                ordo, absc = do_move_road(point.ordo, point.absc, mouvement_optimal[0], rooms, win)
                point = Point(ordo, absc)
                fichier_log.write(point.__str__()+"\n")
                fichier_log.write("\tdistance porte : "+str(point.distance_to(porte_room2))+"\n")
                fichier_log.write("\t\t"+str(point.is_in_voisinage(porte_room2))+"\n")
                liste_points_pad[point.ordo][point.absc][0] = curses.ACS_BOARD
                liste_points_chemin.append(point)
                liste_points_deja_visites.append(point)
    return liste_points_pad
