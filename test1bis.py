#! /usr/bin/env python3
"""
main loop of the program
"""
import time
import curses
import curses.textpad
import subprocess
from monster import create_monsters
from items import *
from player import *
from geometry import Point
from chemin import build_road_between_rooms
from salle import set_player_in_room_random, ramdom_rooms
from methodsCurses import init_curses, set_cursor_visibility,\
     do_move_player, refresh_pad, end_curses, print_all, do_move_and_attack_monsters


ABSC = 0
ORDO = 0
IS_IN_MENU = 0
MAX_ROOMS = 11
NOM = ""
DEBUG = False
stdscr = init_curses()

def enter_is_terminate(x):
    """
    enter is terminate but it's code 7
    """
    if x == 10:
        x = 7
    return x

def begin_game(stdscr):
    """
    the title is better explicit isn't it ?
    """
    global NOM, DEBUG
    stdscr.clear()
    stdscr.refresh()
    curses.noecho()
    win = curses.newwin(1, 60, 0, 0)
    win.addstr(0, 0, "Enter your name here (erase that sentense before !) ", curses.A_BOLD)
    tb = curses.textpad.Textbox(win)
    NOM = tb.edit(enter_is_terminate)
    NOM = NOM.replace(" ", "")
    curses.beep()
    stdscr.addstr(11, 1, "hello "+NOM)
    time.sleep(1)
    curses.start_color()
    curses.use_default_colors()
    colors = []
    rooms = []
    monsters = []
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)
    for index in range(8):
        colors.append(curses.color_pair(index))
    curses.cbreak()
    stdscr.keypad(1)
    pad = curses.newpad(200, 200)
    ordomax , abscmax = pad.getmaxyx()
    stdscr.refresh()
    set_cursor_visibility(0)
    niveau = 1
    player = Player(0, 0)
    while player.is_in_life():
        liste_champ_vision_global = set()
        liste_champ_vision_local = set() 
        liste_points_pad = [[[' ', colors[0]] for absc in range(0, abscmax-1)]for ordo in range(0, ordomax-1)]
        begin_time = time.time()
        key = ''
        liste_points_pad, rooms = ramdom_rooms(pad, min(niveau, MAX_ROOMS)\
            , 5, 5, 15+niveau, 15+niveau, liste_points_pad)
        player.ordo, player.absc = set_player_in_room_random(liste_points_pad)
        liste_points_pad = build_road_between_rooms(rooms, pad, liste_points_pad)
        subprocess.call("logs/check.sh", shell=True)
        liste_points_pad = generate_items(liste_points_pad, colors)
        monsters = create_monsters(niveau, liste_points_pad, colors)
        aff_p_stat = True
        level_sup = False
        while player.is_in_life(): 
            pad.clear()
            if key == ord('q'):
                stdscr.clear()
                stdscr.refresh()
                stdscr.addstr(stdscr.getmaxyx()[0]//2, stdscr.getmaxyx()[1]//2, "Quit ? (y/n)")
                while key != ord('n'):
                    stdscr.refresh()
                    key = stdscr.getch() 
                    if key == ord('y'):
                        end_game(begin_time, player, niveau)
                        return
            if key == ord('e'):
                aff_p_stat = not aff_p_stat

            key = stdscr.getch()
            ORDO, ABSC, level_sup, liste_points_pad = do_move_player(player, pad,\
                 stdscr, key, liste_champ_vision_global, liste_points_pad, monsters, DEBUG)
            monsters = do_move_and_attack_monsters(monsters, player, pad, stdscr, liste_points_pad)
            player.set_player_pos((ORDO, ABSC))
            liste_champ_vision_local = calculate_see_range(player.return_player_pos(), rooms, pad,\
                 liste_points_pad, liste_champ_vision_local)
            liste_champ_vision_global = liste_champ_vision_global.union(liste_champ_vision_local)
            print_all(liste_points_pad,liste_champ_vision_global, liste_champ_vision_local, monsters, pad, DEBUG)
            if level_sup :
                break
            if player.level < 5:
                player.print_player(pad, colors[0])
            elif 5 <= player.level < 10 :
                player.print_player(pad, colors[3])
            elif 10 <= player.level < 15:
                player.print_player(pad, colors[4])
            elif 15 <= player.level < 20:
                player.print_player(pad, colors[2])
            elif 20 <= player.level:
                player.print_player(pad, colors[1])
            if is_player_on_item(liste_points_pad, player.return_player_pos()):
                print_message_item(pad, player.return_player_pos())
            if aff_p_stat:
                player.afficher_player_stats(pad)
            refresh_pad(pad, stdscr, player)
        niveau+=1
    subprocess.call("./logs/clear.sh", shell=True)
    end_game(begin_time, player, niveau)
    end_curses()

def end_game(begin_time, player, niveau):
    """
    too bad ! This is the end
    """
    global NOM 
    score  = player.xp + niveau**2 + player.level**3
    ranc = comprare_score_player_to_the_bests(score)
    if ranc != -1:
        bests = []
        with open("bests.txt", "r") as fichier_scores:
            for line in fichier_scores.readlines():
                line = line.replace("\n", "")
                tuple_line = line.split(" ")
                if int(tuple_line[0]) >= ranc:
                    tuple_line[0] = str(int(tuple_line[0])+1)
                    bests.append(tuple_line)
                elif int(tuple_line[0]) + 1 <= 10:
                    bests.append(tuple_line)
    
        with open("bests.txt", "w") as fichier_scores:
            for tuples in bests:
                fichier_scores.write(str(tuples[0])+" "+tuples[1]+" "+\
                    str(tuples[2])+" "+str(tuples[3])+"\n")
            fichier_scores.write(str(ranc)+" "+NOM+" "+str(score)+" "+\
                str(int(time.time()-begin_time))+"\n")

def comprare_score_player_to_the_bests(score):
    """
    return the ranc of the player , -1 if the player isn't in the top 10 !
    """
    is_empty = True
    lignes_tot = 0
    with open("bests.txt", "r") as fichier_scores:
        for num_l, line in enumerate(fichier_scores.readlines()):
            line = line.replace("\n","")
            tuple_line = line.split(" ")
            if score > int(tuple_line[2]):
                return num_l
            lignes_tot += 1 
            is_empty = False
    return 0 if is_empty else lignes_tot if lignes_tot <= 10 else -1

    
def main(stdscr):
    """
    Print the welcoming menu ! 
    """
    global IS_IN_MENU


    stdscr.leaveok(1)
    set_cursor_visibility(0) 
    menus = [" PLay ", " About ", " Best Scores ", " Quit Game"]
    attr = [curses.A_NORMAL for i in range(len(menus))]
    attr[0] = curses.A_BOLD 
    stdscr.leaveok(0)
    index_menus = 0
    curses.setsyx(-1, -1)

    while IS_IN_MENU != 1:
        ymax, xmax = stdscr.getmaxyx()
        y_middle, x_middle = ymax//2, xmax//2

        while abs(ymax -y_middle) < len(menus) :
            ymax, xmax = stdscr.getmaxyx()
            y_middle, x_middle = ymax//2, xmax//2
            stdscr.clear()
        while abs(xmax -x_middle) < len(menus) :
            ymax, xmax = stdscr.getmaxyx()
            y_middle, x_middle = ymax//2, xmax//2
            stdscr.clear()  

        stdscr.addstr(y_middle, x_middle, "Welcome to Pyhack Game ! \n ",curses.A_BOLD)
        stdscr.addstr(y_middle+1, x_middle, "A game by Nathan DAUNOIS ", curses.A_BOLD)
        stdscr.addstr(y_middle+2, x_middle, "Grenoble-Inp-Ensimag ", curses.A_BOLD)
        stdscr.addstr(y_middle+3, x_middle, "choose with (8-2) select with enter", curses.A_BOLD)

        print_items_list_selection(stdscr, attr, y_middle, x_middle, menus)
        key = stdscr.getch()
        if key == ord('2'):
            if index_menus+1 < len(menus):
                attr[index_menus] = curses.A_NORMAL
                index_menus += 1 
                attr[index_menus] = curses.A_BOLD
        elif key == ord('8'):
            if index_menus - 1 >= 0:
                attr[index_menus] = curses.A_NORMAL
                index_menus -= 1
                attr[index_menus] = curses.A_BOLD
        elif enter_is_terminate(key) == 7:
            IS_IN_MENU = apply_choice_player_in_menu(stdscr, menus, index_menus)
            if not IS_IN_MENU:
                return
        stdscr.refresh()
        stdscr.clear()     
    begin_game(stdscr)

def apply_choice_player_in_menu(stdscr, menus, index):
    """
    apply the choice of the player
    """
    if index == 0:
        return 1
    elif index == 1:
        subprocess.call("evince about.pdf", shell=True)
        return 2
    elif index == 2:
        key = ''
        while key != ord('q'):
            stdscr.clear()
            stdscr.refresh()
            ymax, xmax = stdscr.getmaxyx()
            y_middle, x_middle = ymax//2, xmax//2

            while abs(ymax-y_middle) < len(menus) :
                ymax, xmax = stdscr.getmaxyx()
                y_middle, x_middle = ymax//2, xmax//2
                stdscr.clear()
            while abs(xmax-x_middle) < len(menus) :
                ymax, xmax = stdscr.getmaxyx()
                y_middle, x_middle = ymax//2, xmax//2
                stdscr.clear()
            
            stdscr.addstr(y_middle, x_middle, "les meilleurs :\n", curses.A_BOLD)
            with open("bests.txt", "r") as fichier_scores:
                bests = []
                for line in fichier_scores.readlines():
                    line = line.replace("\n", "")
                    tuple_line = line.split(" ")
                    bests.append(tuple_line)
                index = 0
                while len(bests) > 0:
                    for tuples in bests:
                        if int(tuples[0]) == index:
                            stdscr.addstr(y_middle+index, x_middle, tuples[1]+" score: "+str(tuples[2])+" tps: "+str(tuples[3]), curses.A_BOLD)
                            del bests[bests.index(tuples)]
                            index += 1
            stdscr.border(curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_HLINE,\
            curses.ACS_HLINE, curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LLCORNER, curses.ACS_LRCORNER)
            key = stdscr.getch()
        return 2
    elif index == 4:
        return 0
    return 0

def print_items_list_selection(stdscr, attr, y_middle, x_middle, menus):
    """
    print all the choices the player can select
    """

    for index, menu in enumerate(menus):
        if attr[index] == curses.A_BOLD:
            stdscr.addch(y_middle+5+index, x_middle, curses.ACS_RARROW, attr[index])
            stdscr.addstr(y_middle+5+index, x_middle+1, menu, attr[index])
            stdscr.addch(y_middle+5+index, x_middle+len(menu)+1, curses.ACS_LARROW, attr[index])
            stdscr.addstr(y_middle+5+index, x_middle+len(menu)+2, "  ", attr[index])
        else:
            stdscr.addstr(y_middle+5+index, x_middle, menu+"  ", attr[index])
        
    stdscr.border(curses.ACS_VLINE, curses.ACS_VLINE, curses.ACS_HLINE,\
        curses.ACS_HLINE, curses.ACS_ULCORNER, curses.ACS_URCORNER, curses.ACS_LLCORNER, curses.ACS_LRCORNER)

main(stdscr)
