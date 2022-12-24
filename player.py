#!/urs/bin/env python3

"""
the class of the player !!!!
"""
import curses
from time import sleep
from geometry import Point
from methodsCurses import do_move_player , set_cursor_visibility, refresh_pad, print_all
from monster import Boss

MAX_SEE_RANGE = 8
CALCULATE = True
# juste here in order to ignore calculs if the room is already discovered ! 

class Player():
    """
    the "me" in th game
    """
    def __init__(self, ordo, absc):
        self.ordo = ordo
        self.absc = absc
        self.pv = 200
        self.pv_limit = 200
        self.armor = 0
        self.att = 1
        self.xp = 0
        self.xp_limit = 10
        self.level = 0
        self.number_of_arrow = 10 # The player can't have a unlimited source of arrow !

    def print_player(self, win, color):
        """
        print player
        """
        win.addstr(self.ordo, self.absc, "@", color)
    def set_player_pos(self, tuple_pos):
        """
        nothing to add
        """
        self.ordo = tuple_pos[0]
        self.absc = tuple_pos[1]
    
    def return_player_pos(self):
        """
        return player pos
        """
        return Point(self.ordo, self.absc)
    
    def afficher_player_stats(self, win):
        """
        print player stats
        """
        ordo, absc = max(0, self.ordo-20), max(0, self.absc-20)
        win.addstr(ordo, absc, "Pv : {0}/{1} Armor : {2} Att : {3}  Arrows : {4}\
             ".format(self.pv, self.pv_limit, self.armor, self.att,\
            self.number_of_arrow))
        win.addstr(ordo+1, absc, "xp : {0}/{1} Level_player : {2}  ".format(self.xp, self.xp_limit, self.level))


    def attack_c(self, monsters, with_bow=False, **kwargs):
        """
        att contact
        """
        ordo = kwargs.get('ordo', None)
        absc = kwargs.get('absc', None)

        for monster in monsters:
            if with_bow:
                if Point(ordo, absc) == monster.return_pos():
                    monster.pv -= max(self.att-monster.armor, 0)
                    self.xp += 2*monster.ac if isinstance(monster, Boss) else monster.ac
            else:
                if self.return_player_pos().is_in_voisinage(monster.return_pos()):
                    monster.pv -= max(self.att-monster.armor, 0)
                    self.xp += 2*monster.ac if isinstance(monster, Boss) else monster.ac
            while self.xp >= self.xp_limit:
                self.level += 1
                self.pv_limit += 20
                self.pv += 20
                self.xp %= self.xp_limit
                self.xp_limit += (5*self.level)

    def attack_d(self, monsters, liste_champ_vision, liste_points_pad, win, pad, debug=True):
        """
        att distance
        """
        def is_in_list(listes, point):
            """
            lol
            """
            for elts in listes:
                for elt in elts:
                    if point == elt:
                        return True
            return False

        def print_list(liste, pad, liste_points_pad):
            """
            print the list
            """
            for elts in liste:
                for elt in elts:
                    tuple_to_print = liste_points_pad[elt.absc][elt.ordo]
                    pad.addch(elt.ordo, elt.absc,tuple_to_print[0], tuple_to_print[1])
            for monster in monsters:
                 if monster.is_in_life():
                    if debug:
                        monster.print_monster(pad)
                    else:
                        if Point(monster.ordo, monster.absc) in liste_champ_vision:
                            monster.print_monster(pad)

        def del_in_list(liste, liste_champ_vision):
            """
            Delete all the points that are not in liste_champ_vision
            """
            for elts in liste:
                for elt in elts:
                    if not (elt in liste_champ_vision):
                        try:
                            del liste[liste.index(elt)]
                        except ValueError:
                            continue
            return liste

        list_range_arrows = [[Point(self.ordo+ordo, self.absc+absc)for ordo in range(-2, 3)]for absc in range(-2, 3)]
        if not debug:
            list_range_arrows = del_in_list(list_range_arrows, liste_champ_vision)

        key = ' '
        set_cursor_visibility(2)
        ordo, absc = self.ordo, self.absc
        pad.move(absc, ordo)
        curses.noecho()
        while key != ord('q'):
            key = pad.getch()
            self.afficher_player_stats(pad)
            print_list(list_range_arrows, pad, liste_points_pad)
            if key == ord('4'):
                if is_in_list(list_range_arrows, Point(ordo, absc-1)):
                    absc-=1 
            elif key == ord('6'):
                if is_in_list(list_range_arrows, Point(ordo, absc+1)):
                    absc+=1
            elif key == ord('2'):
                if is_in_list(list_range_arrows, Point(ordo+1, absc)):
                    ordo+=1
            elif key == ord('8'):
                if is_in_list(list_range_arrows, Point(ordo-1, absc)):
                    ordo-=1
            elif key == ord('d'):
                if self.number_of_arrow >=1:
                    self.attack_c(monsters, with_bow=True, ordo=ordo, absc=absc)
                    self.number_of_arrow-=1
            pad.move(ordo, absc)
            refresh_pad(pad, win, self)
        win.leaveok(1)
        set_cursor_visibility(0) 

    def is_in_life(self) :
        return self.pv > 0

def calculate_see_range(player, rooms, win, liste_points_pad, liste_points_vision):
    """
    Calculate what the player can see

    In coridor : 1 square of 1
    In room : everything , and if the player is near a door , print all the line from the player to the wall 
    """
    ordo_max, absc_max = win.getmaxyx()
    liste = set()
    global CALCULATE
    if liste_points_pad[player.absc][player.ordo][0] == '.':
        if CALCULATE:
            liste_points_vision.update(add_points(player, liste, liste_points_pad))
            CALCULATE = False
    else:
        CALCULATE = True
        liste_points_vision.clear()
    for ordo in range(-1, 2):
        for absc in range(-1, 2):
            point_bis = Point(player.ordo+ordo, player.absc+absc)
            if player.absc+absc in [-1, absc_max-1] or player.ordo+ordo in [-1, ordo_max-1]:
                liste_points_vision.add(Point(0, 0))
            else:
                liste_points_vision.add(point_bis)
    return liste_points_vision

def add_points(point, liste, liste_points_pad):
    """
    add recurcively all the points of a room
    """
    try:
        if liste_points_pad[point.absc][point.ordo][0] in ['.', curses.ACS_VLINE, curses.ACS_HLINE, curses.ACS_ULCORNER \
, curses.ACS_LLCORNER, curses.ACS_URCORNER, curses.ACS_LRCORNER] and point not in liste:
            liste.add(point)
            liste = add_points(point.addpointy(-1), liste, liste_points_pad)
            liste = add_points(point.addpointy(+1), liste, liste_points_pad)
            liste = add_points(point.addpointx(-1), liste, liste_points_pad)
            liste = add_points(point.addpointx(+1), liste, liste_points_pad)
    except IndexError:
        return liste
    return liste
