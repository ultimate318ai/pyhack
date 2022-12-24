#! /usr/bin/env python3
"""
Room class ... central point of the game
"""
import curses
from random import randint
from geometry import Point


class Room():
    """
    A rooooomm !
    """
    def __init__(self, pointhautg, largeur, hauteur):
        """
        create the room by putting all the point of the room in lists
        """
        self.pointhautg = (pointhautg if isinstance(pointhautg, Point) else None)
        self.largeur = largeur
        self.hauteur = hauteur
        liste_points_inter_salle = []
        liste_points_murs = []
        liste_hlines = []
        liste_vlines = []
        liste_portes = []
        liste_points_tot = []
        for ordo in range(pointhautg.ordo, pointhautg.ordo+hauteur+1):
            for absc in range(pointhautg.absc, pointhautg.absc+largeur+1):
                if ordo not in [pointhautg.ordo, pointhautg.ordo+hauteur] \
                    and absc not in [pointhautg.absc, pointhautg.absc+largeur]:
                    liste_points_inter_salle.append(Point(ordo, absc))
                else:
                    if ordo == pointhautg.ordo or ordo == pointhautg.ordo+hauteur:
                        liste_hlines.append(Point(ordo, absc))
                    else:
                        liste_vlines.append(Point(ordo, absc))
                    liste_points_murs.append(Point(ordo, absc))
                liste_points_tot.append(Point(ordo, absc))
        nb_portes = randint(1, 4)
        while len(liste_portes) < nb_portes:
            porte = liste_points_murs[randint(0, len(liste_points_murs)-1)]
            if porte not in [pointhautg, pointhautg.addpointx(largeur),\
                pointhautg.addpointy(hauteur), pointhautg.addpointxy(largeur, hauteur)]:
                liste_portes.append(porte)
                del liste_points_murs[liste_points_murs.index(porte)]

        self.liste_points_inter_salle = liste_points_inter_salle
        self.liste_points_murs = liste_points_murs
        self.liste_portes = liste_portes
        self.liste_points_tot = liste_points_tot
        self.liste_hlines = liste_hlines
        self.liste_vlines = liste_vlines

def random_room(pad, room_min_largeur, room_min_hauteur, room_max_largeur, room_max_hauteur):
    """
    create a random room
    """
    assert room_max_largeur - room_min_largeur > 0 and \
        room_max_hauteur - room_min_hauteur > 0
    maxypad, maxxpad = pad.getmaxyx()
    point = Point(randint(1, maxxpad-room_min_largeur-1), randint(1, maxypad-room_min_hauteur-1))
    return Room(point,min(randint(room_min_largeur, room_max_largeur)\
        ,abs(point.absc-maxxpad) -1),\
        min(randint(room_min_hauteur, room_max_hauteur), abs(point.ordo- maxypad) -1))

def ramdom_rooms(pad, number, room_min_largeur, room_min_hauteur,\
     room_max_largeur, room_max_hauteur, liste_points_pad):
    """
    create number random rooms
    """
    if number <= 0:
        return None
    rooms = []
    while number > 0:
        room = random_room(pad, room_min_largeur,\
             room_min_hauteur, room_max_largeur, room_max_hauteur)
        if test_room(room, liste_points_pad):
            for point in room.liste_hlines:
                liste_points_pad[point.ordo][point.absc][0] = curses.ACS_VLINE
            for point in room.liste_vlines:
                liste_points_pad[point.ordo][point.absc][0] = curses.ACS_HLINE
            # Corner add
            liste_points_pad[room.pointhautg.ordo][room.pointhautg.absc][0]\
                = curses.ACS_ULCORNER
            liste_points_pad[room.pointhautg.ordo][room.pointhautg.absc+room.largeur][0]\
                = curses.ACS_LLCORNER
            liste_points_pad[room.pointhautg.ordo+room.hauteur][room.pointhautg.absc][0]\
                = curses.ACS_URCORNER
            liste_points_pad[room.pointhautg.ordo+room.hauteur][room.pointhautg.absc+room\
                .largeur][0]\
                = curses.ACS_LRCORNER
            for point in room.liste_points_inter_salle:
                liste_points_pad[point.ordo][point.absc][0] = '.'
            for point in room.liste_portes:
                liste_points_pad[point.ordo][point.absc][0] = '.'
            rooms.append(room)
            number -= 1
    return liste_points_pad, rooms

def test_room(room, liste_points_pad):
    """
    check if a room have not been created in another !
    """
    for point in room.liste_points_murs:
        try:
            if liste_points_pad[point.ordo][point.absc][0] != ' ':
                return False
        except IndexError :
            return False
    for porte in room.liste_portes:
        counter = 0
        for point in [Point(porte.ordo+1, porte.absc), Point(porte.ordo-1, porte.absc)\
            , Point(porte.ordo, porte.absc+1), Point(porte.ordo, porte.absc-1)]:
            try:
                if liste_points_pad[point.ordo][point.absc][0] == ' ':
                    counter += 1
            except IndexError:
                continue
        if not counter:
            return False
    return True

def set_player_in_room_random(liste_points_pad):
    """
    Put the player in a random room
    """
    pos = ' '
    absc = 0
    ordo = 0
    while pos != '.':
        absc = randint(0, len(liste_points_pad[0])-1)
        ordo = randint(0, len(liste_points_pad)-1)
        pos = liste_points_pad[ordo][absc][0]
    return absc, ordo 
