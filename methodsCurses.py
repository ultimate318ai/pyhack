#! /usr/bin/env python3
"""
All methods of curses simplified in order of not have a code too messy
"""
import curses
from random import randint
from geometry import Point
from items import is_player_on_item, apply_changement 
from monster import Monster, Boss 


def init_curses():
    """
    init
    """
    return curses.initscr() 

def end_curses():
    """
    So this is the end ... , turn your back and count .... to ten (etc) ref=Adele
    """
    curses.endwin()

def set_cursor_visibility(level):
    """
    change th cusor visibility
    """
    curses.curs_set(level if level in [0, 1, 2] else 1)

def do_move_road(ordo,absc,key,rooms,win):
    """
    the mooves for the roads
    """
    if key == curses.KEY_LEFT:
        absc -= 1 
    elif key == curses.KEY_RIGHT:
        absc += 1
    elif key == curses.KEY_DOWN:
        ordo += 1
    elif key == curses.KEY_UP:
        ordo -= 1
    return ordo, absc

def set_getch_nonblock(win):
    """
    set getch non bloc
    """
    win.nodelay(1)

def refresh_pad(pad, win, player):
    """
    refresh the pad
    """
    absc, ordo = player.absc, player.ordo
    rows, cols = win.getmaxyx()
    dimy, dimx = pad.getmaxyx()
    pad_centrage = Point(max(0, min(dimy-rows , ordo-rows//2)),\
        max(0, min(dimx-cols, absc-cols//2)))
    pad.refresh(pad_centrage.ordo, pad_centrage.absc, 0, 0, rows-1, cols-1)

def is_coordinate_valid_after_movment_road(ordo, absc, rooms, win, liste_points_interdis, liste_points_pad):
    """
    check is the moovment is valid ! 
    """
    ymax, xmax = win.getmaxyx()
    if absc in [-1, xmax-1] or ordo in [-1, ymax-1] or Point(ordo, absc) in liste_points_interdis:
        return False
    return liste_points_pad[ordo][absc][0] == ' ' or liste_points_pad[ordo][absc][0] == curses.ACS_BOARD

def do_move_player(player, win, screen, key, liste_champ_vision, liste_points_pad, monsters, debug=True):
    """
    apply the moovment for the player (if possible)
    """
    absc, ordo  = player.absc, player.ordo
    is_level_up = False
    if key == curses.KEY_LEFT:
        if is_coordinate_valid_after_movment(win, ordo, absc-1, liste_points_pad):
            absc -= 1 
    elif key == curses.KEY_RIGHT:
        if is_coordinate_valid_after_movment(win, ordo, absc+1, liste_points_pad):
            absc += 1
    elif key == curses.KEY_DOWN:
        if is_coordinate_valid_after_movment(win, ordo+1, absc, liste_points_pad):
            ordo += 1
    elif key == curses.KEY_UP:
        if is_coordinate_valid_after_movment(win, ordo-1, absc, liste_points_pad):
            ordo -= 1
    elif key == ord('7'):
        if is_coordinate_valid_after_movment(win, ordo-1, absc-1, liste_points_pad):
            absc -= 1
            ordo -= 1
    elif key == ord('9'):
        if is_coordinate_valid_after_movment(win, ordo-1, absc+1, liste_points_pad):
            absc += 1
            ordo -= 1
    elif key == ord('3'):
        if is_coordinate_valid_after_movment(win, ordo+1, absc+1, liste_points_pad):
            absc += 1
            ordo += 1
    elif key == ord('1'):
        if is_coordinate_valid_after_movment(win, ordo+1, absc-1, liste_points_pad):
            absc -= 1
            ordo += 1
    elif key == ord('o'):
        number = is_player_on_item(liste_points_pad, Point(ordo, absc))
        if number:
            liste_points_pad, player, is_level_up = apply_changement(liste_points_pad, player)
    elif key == ord('c'):
        player.attack_c(monsters)
    elif key == ord('d'):
        player.attack_d(monsters, liste_champ_vision, liste_points_pad, screen, win, debug=debug)
           
    return ordo, absc , is_level_up , liste_points_pad

def do_move_and_attack_monsters(monsters, player, win, stdscr, liste_points_pad):
    """
    moovment for the monsters
    """
    mouvments = [curses.KEY_LEFT, curses.KEY_RIGHT , curses.KEY_DOWN, curses.KEY_UP,\
        curses.KEY_LEFT, curses.KEY_RIGHT , curses.KEY_DOWN, curses.KEY_UP, ord('7')\
        , ord('9'), ord('3'), ord('1')]
    for monster in monsters:
        if not monster.is_in_life():
            del monsters[monsters.index(monster)]
            continue
        absc, ordo  = monster.absc, monster.ordo
        if monster.return_pos().is_in_voisinage(player.return_player_pos()):
            monster.attack_c(player)
        else:
            if isinstance(monster, Boss):
                if monster.return_pos().distance_to(player.return_player_pos()) < 18:
                    monster.attack_d(player)
            mouvment = mouvments[randint(0, len(mouvments)-1)]
            if mouvment == curses.KEY_LEFT:
                if is_coordinate_valid_after_movment(win, ordo, absc-1, liste_points_pad) and absc-1 != player.absc:
                    absc -= 1 
            elif mouvment == curses.KEY_RIGHT:
                if is_coordinate_valid_after_movment(win, ordo, absc+1, liste_points_pad)and absc+1 != player.absc:
                    absc += 1
            elif mouvment == curses.KEY_DOWN:
                if is_coordinate_valid_after_movment(win, ordo+1, absc, liste_points_pad) and ordo+1 != player.ordo:
                    ordo += 1
            elif mouvment == curses.KEY_UP:
                if is_coordinate_valid_after_movment(win, ordo-1, absc, liste_points_pad)and ordo-1 != player.ordo:
                    ordo -= 1
            elif mouvment == ord('7'):
                if is_coordinate_valid_after_movment(win, ordo-1, absc-1, liste_points_pad)\
                    and ordo-1 != player.ordo and absc-1 != player.absc:
                    absc -= 1
                    ordo -= 1
            elif mouvment == ord('9'):
                if is_coordinate_valid_after_movment(win, ordo-1, absc+1, liste_points_pad)\
                    and ordo-1 != player.ordo and absc+1 != player.absc:
                    absc += 1
                    ordo -= 1
            elif mouvment == ord('3'):
                if is_coordinate_valid_after_movment(win, ordo+1, absc+1, liste_points_pad)\
                    and ordo+1 != player.ordo and absc+1 != player.absc:
                    absc += 1
                    ordo += 1
            elif mouvment == ord('1'):
                if is_coordinate_valid_after_movment(win, ordo+1, absc-1, liste_points_pad)\
                    and ordo+1 != player.ordo and absc-1 != player.absc:
                    absc -= 1
                    ordo += 1
            monster.absc, monster.ordo = absc, ordo
    return monsters

def is_coordinate_valid_after_movment(win, ordo, absc, liste_points_pad):
    """
    check if the new coordinate is good or not
    """
    ymax,xmax = win.getmaxyx()
    if absc in [-1, xmax-1] or ordo in [-1, ymax-1] :
        return False
    return str(liste_points_pad[absc][ordo][0]) in ".+%?=[]()#$!"\
     or liste_points_pad[absc][ordo][0] in [curses.ACS_BOARD]
def print_all(liste_points_pad, liste_champ_vision_global , liste_champ_vision_local, monsters, win, debug=True):
    """
    print all the symbols
    """
    if not debug:
        for point in liste_champ_vision_global:
            ordo, absc = point.ordo, point.absc
            win.addch(ordo, absc, liste_points_pad[absc][ordo][0], liste_points_pad[absc][ordo][1])
    else:
        for absc, symbols in enumerate(liste_points_pad):
            for ordo, tuple_symbol in enumerate(symbols):
                win.addch(ordo, absc, tuple_symbol[0], tuple_symbol[1])
    for monster in monsters:
        if monster.is_in_life():
            if debug:
                monster.print_monster(win)
            else:
                if Point(monster.ordo, monster.absc) in liste_champ_vision_local:
                    monster.print_monster(win)
