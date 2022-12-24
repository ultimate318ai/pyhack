#!/usr/bin/env python3


import curses
from random import randint
from geometry import Point

def generate_items(liste_points_pad, colors):
    """
    generate the items
    """
    pos = ' '
    absc = 0
    ordo = 0
    while str(pos) not in ".":
        absc = randint(0, len(liste_points_pad[0])-1)
        ordo = randint(0, len(liste_points_pad)-1)
        pos = liste_points_pad[ordo][absc][0]       
    liste_points_pad[ordo][absc][0] = "$"
        
    for index in range(0, randint(1, 4)):
        pos = ' '
        if randint(0, 100) <= 50:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
                
            liste_points_pad[ordo][absc] = "+", colors[3]
        if randint(0, 100) <= 15:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
                
            liste_points_pad[ordo][absc] = "%", colors[1]
        if randint(0, 100) <= 10:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
                
            liste_points_pad[ordo][absc] = "!", colors[3]
        if randint(0, 100) <= 10 and index == 1:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
                
            liste_points_pad[ordo][absc] = "=", colors[3]
        if randint(0,100) <= 25:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
                
            liste_points_pad[ordo][absc] = "?", colors[2]
        if randint(0,100) <= 17:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
                
            liste_points_pad[ordo][absc] = "(", colors[5]
        if randint(0,100) <= 17:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
                
            liste_points_pad[ordo][absc] = ")", colors[5]
        if randint(0,100) <= 8:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
                
            liste_points_pad[ordo][absc] = "[", colors[5]
        if randint(0,100) <= 8:
            while pos != '.':
                absc = randint(0, len(liste_points_pad[0])-1)
                ordo = randint(0, len(liste_points_pad)-1)
                pos = liste_points_pad[ordo][absc][0]
        
                
            liste_points_pad[ordo][absc] = "]", colors[5]
    return liste_points_pad

def is_player_on_item(liste_points_pad, point_j):
    return str(liste_points_pad[point_j.absc][point_j.ordo][0]) in "+=!?%[]()$#" 

def print_message_item(win, point_j):
    ordo, absc = max(0, point_j.ordo -18), max(0, point_j.absc -20)
    win.addstr(ordo, absc, "take this item ?(o)")

def apply_changement(liste_points_pad, player):
    """
    if the player took the item : apply changements
    """
    item = liste_points_pad[player.absc][player.ordo][0]
    is_level_up = False
    if item == '$':
        pos = ' '
        absc = randint(0, len(liste_points_pad[0])-1)
        ordo = randint(0, len(liste_points_pad)-1)
        while pos != '.':
            absc = randint(0, len(liste_points_pad[0])-1)
            ordo = randint(0, len(liste_points_pad)-1)
            pos = liste_points_pad[ordo][absc][0]
        liste_points_pad[ordo][absc] = "#", 0
    elif item == '+':
        if (player.pv < player.pv_limit): 
            player.pv = player.pv + 50 if player.pv + 50 <= player.pv_limit else player.pv + (player.pv_limit-player.pv)
        player.number_of_arrow += 5
    elif item == '?':
        player.pv = player.pv + randint(-100, 300)
    elif item == '!':
        player.pv = player.pv + randint(0, 200)
    elif item == '=': 
        player.pv = max(player.pv, player.pv_limit)
        player.number_of_arrow += 30
    elif item == '%':
        player.att += 1
    elif item in "[]":
        player.armor += 2
    elif item in "()":
        player.armor += 1
    elif item == "#":
        is_level_up = True
    liste_points_pad[player.absc][player.ordo] = '.', 0
    return liste_points_pad, player, is_level_up
