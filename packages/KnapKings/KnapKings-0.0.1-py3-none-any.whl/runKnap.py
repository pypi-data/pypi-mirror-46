import Knapsack as k
# ----------------------------
CMD_LINE = True # set True for cmd line interaction. otherwise modify globals below
# ----------------------------

ENTRIES = 1

# sport
BASK = True
BASE = False

# contest websites
FD = True   # FanDuel
DK = True  # DraftKings
CAP = False  # Captain Showdown
MULTI = False # Multi Entry
# -----------------------

# projection websites
GRIND = True    # RotoGrinders
NUM_FIRE = False # NumberFire
# ------------------------

# lineup modifications
DROP_PLAYERS = set() # players to remove from lineup, must be type set
LOCK_PLAYERS = set() # players to secure in lineup, must be type set
# ------------------------


def main():

    if CMD_LINE: user_input()

    if BASK:

        if MULTI:
            if FD:
                contest = "fanduel"
                if NUM_FIRE:
                    system = "numberfire"
                    k.multipleOptimizer(contest,system,ENTRIES)
                if GRIND:
                    system = "rotogrinders"
                    k.multipleOptimizer(contest,system,ENTRIES)
            if DK:
                contest = "draftkings"
                system = "rotogrinders"
                k.multipleOptimizer(contest,system,ENTRIES)
            return
            
        if FD:

            if NUM_FIRE:
                k.fanduelOptimizer('numberfire', LOCK_PLAYERS, DROP_PLAYERS)

            if GRIND:
                k.fanduelOptimizer('rotogrinders', LOCK_PLAYERS, DROP_PLAYERS)

        if DK:

            if NUM_FIRE:
                print('ERROR: NumberFire projections are unavailable for DraftKings contests.')

            if GRIND:
                k.draftkingsOptimizer('rotogrinders', LOCK_PLAYERS, DROP_PLAYERS)



    if BASE:
        k.baseballOptimizer(LOCK_PLAYERS, DROP_PLAYERS)


def user_input():
    global FD, DK, NUM_FIRE, GRIND, LOCK_PLAYERS, DROP_PLAYERS, BASE, BASK, MULTI, ENTRIES

    print('-'*10 + '\n * Welcome to the daily fantasy sports lineup optimizer.\n * Please type the number that corresponds to your choice followed by the return key.')
    # sport selection
    sport = input('\n * Select a sport:\n * 1. Basketball\n * 2. Baseball (FanDuel+NumberFire only)\n-> ')
    while sport.isdigit() == False or int(sport) > 2 or int(sport) < 1:
        sport = input('\n * Error: Please enter valid numbers only.\n * Select a sport:\n * 1. Basketball\n * 2. Baseball (FanDuel+NumberFire only)\n-> ')
    sport = int(sport)
    if sport == 1:
        BASK = True
        BASE = False
    elif sport == 2:
        BASK = False
        BASE = True
        print('\n * FanDuel selected as contest website.')
        print(' * NumberFire selected as projection website.')

        
    

    if BASK:
        # contest website
        contest = input('\n * Select a contest website. Note that if you select \'DraftKings\' or \'Both\', NumberFire will not be an available projection website:\n * 1. FanDuel\n * 2. DraftKings\n * 3. Both\n-> ')
        while contest.isdigit() == False or int(contest) > 3 or int(contest) < 1:
            contest = input('\n * Error: Please enter valid numbers only.\n * Select a contest website. Note that if you select \'DraftKings\' or \'Both\', NumberFire will not be an available projection website:\n * 1. FanDuel\n * 2. DraftKings\n * 3. Both\n-> ')
        contest = int(contest)
        FD = True if (contest == 1 or contest == 3) else False
        DK = True if (contest == 2 or contest == 3) else False

        # projection website
        if contest == 1:
            proj = input('\n * Select a projection website:\n * 1. NumberFire\n * 2. RotoGrinders\n * 3. Both\n-> ')
            while proj.isdigit() == False or int(proj) > 3 or int(proj) < 1:
                proj = input('\n * Error: Please enter valid numbers only.\n * Select a projection website:\n * 1. NumberFire\n * 2. RotoGrinders\n * 3. Both\n-> ')
            proj = int(proj)

            NUM_FIRE = True if (proj == 1 or proj == 3) else False
            GRIND = True if (proj == 2 or proj == 3) else False
        else:
            print('\n * RotoGrinders selected as the projection website.')
            GRIND = True
            NUM_FIRE = False

        # single or multiple lineups
        ENTRIES = input('\n * Enter the number of lineups you want the program to output (1-20).\n * If you enter more than 1, locking/dropping players will be unavailable.\n-> ')
        while ENTRIES.isdigit() == False or int(ENTRIES) < 1 or int(ENTRIES) > 20:
            ENTRIES = input('\n * Error: Please enter valid numbers only.\n * Enter the number of lineups you want the program to output (1-20).\n-> ')
        ENTRIES = int(ENTRIES)
        if ENTRIES > 1:
            MULTI = True
            return

    # locked players
    lock = input('\n * Enter the names of the players who you want to lock into all your lineups followed by the return key (comma separated, one space in between).\n * Or, click the return key to lock no players.\n * Ex: Kevin Durant, Kyrie Irving\n-> ')
    LOCK_PLAYERS = set(lock.split(', ')) if len(lock) > 0 else set()

    # excluded players
    drop = input('\n * Enter the names of the players who you want to exclude from all your lineups followed by the return key (comma separated, one space in between).\n * Or, click the return key to exclude no players.\n-> ')
    DROP_PLAYERS = set(drop.split(', ')) if len(drop) > 0 else set()


main()