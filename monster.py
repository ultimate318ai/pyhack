"""
all things about the monsters grrrr !
"""
import curses
from random import randint
from geometry import Point

BOSS = 0
BOSSES = ["\u03B5", "\u03C0", "@", "\u221e"] #symbols used for the boss

class Monster():
    """
    grrrr
    """
    def __init__(self, ordo, absc, symbol, armor, pv, color, att_c=0):
        self.symbol = symbol
        self.ordo = ordo
        self.absc = absc
        self.pv = pv
        self.armor = armor
        self.ac = att_c
        self.color = color

    def print_monster(self, win):
        """
        print the monsters
        """
        win.addstr(self.ordo, self.absc, self.symbol, self.color)  

    def is_in_life(self):
        """
        is the monster dead ?
        """
        return self.pv > 0
    def return_pos(self):
        """
        return the pos of the monster (with a point)
        """
        return Point(self.ordo, self.absc)

    def attack_c(self, player):
        """
        the monster attack the player
        """
        curses.beep()
        if self.symbol not in ["\u00BC", "\u00BD", "\u00BE", "\u00BF", "\u00A1"]: 
            player.pv -= max(self.ac-player.armor, 0)
        else:
            if self.symbol == "\u00BC":
                player.pv //= 4
            elif self.symbol == "\u00BD":
                player.pv //= 2
            elif self.symbol == "\u00BE":
                player.pv //= (4/3)
            elif self.symbol == "\u00BF":
                player.pv += randint(-80, 50)
            elif self.symbol == "\u00A1":
                player.pv -= randint(0, 50)

class Boss(Monster):
    """
    that type of monster isn't very kind !
    """
    def __init__(self, ordo, absc, symbol, armor, pv, color, att_c=0, att_d=0):
        Monster.__init__(self, ordo, absc, symbol, armor, pv, color, att_c)
        self.att_d = att_d

    def attack_d(self, player):
        """
        distance attack
        """
        curses.beep()
        if self.symbol == "\u221e":
            player.pv -= 10
        elif self.symbol == "\u03C0":
            player.pv -= 3
        elif self.symbol == "@":
            player.pv -= 8
        elif self.symbol == "\u03B5":
            player.pv -= 1

    def print_monster(self, win):
        Monster.print_monster(self, win)

def create_monsters(niveau, liste_points_pad, colors):
    """
    create the monsters and return the list monsters containing all the monsters
    """
    monsters = []
    global BOSS , BOSSES
    absc , ordo = return_valid_position(liste_points_pad)

    for _ in range(randint(niveau-1, (niveau*(niveau-1 if niveau > 1 else 1))//2)+1):
        monster_type = randint(niveau-1 , min(niveau*2, 78)) # x between 0 and 78
        letter_monster = chr((97+(monster_type%26)))
        color_monster = colors[4] if monster_type < 27 else colors[2] if monster_type < 52 else colors[1]
        absc , ordo = return_valid_position(liste_points_pad)
        monster = Monster(absc , ordo, letter_monster,\
            0, monster_type%26+1, color_monster, monster_type+1)
        monsters.append(monster)

    symbols_specials = ["\u00BC", "\u00BD", "\u00BE", "\u00BF", "\u00A1"]
    if not niveau % 2:
        absc , ordo = return_valid_position(liste_points_pad)
        monster_special = Monster(absc, ordo,\
            symbols_specials[randint(0, len(symbols_specials)-1)] , 0, 10, colors[3], 0)
        monsters.append(monster_special)
    if not niveau % 5:
        absc , ordo = return_valid_position(liste_points_pad)
        monsters.append(Boss(absc, ordo, BOSSES[BOSS], BOSS, 5*(BOSS+1)+niveau,\
            colors[1], 10*(BOSS+1), (BOSS+1)**2))
        BOSS = BOSS+1 if BOSS < len(BOSSES) else 0

    return monsters

def return_valid_position(liste_points_pad):
    """
    a monster should be placed in a room or in a road
    """
    pos = ' '
    absc = 0
    ordo = 0
    while pos  != '.':
        absc = randint(0, len(liste_points_pad[0])-1)
        ordo = randint(0, len(liste_points_pad)-1)
        pos = liste_points_pad[ordo][absc][0]
    return absc, ordo 
