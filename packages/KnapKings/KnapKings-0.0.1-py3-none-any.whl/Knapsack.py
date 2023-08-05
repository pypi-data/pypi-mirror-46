"""
This module maximizes the value of a roster for a given set of players
"""
import numpy as np
import csv
from Player import player 
import requests
import urllib.request
from bs4 import BeautifulSoup
import re
import datetime
from random import shuffle


CUR_DATE = str(datetime.datetime.now())[:10]

def optimize(players, budget):
    """
    Generates the optimal lineup for DraftKings based on player projections.

    Inputs:
        players: 2-D array containing player objects for each player by position
        num_players: total number of players
        budget: amount of money to spend on players
    """
    
    num_pos = len(players)
    
    V = np.zeros((num_pos, budget+1))   # array to track max vorp
    Who = np.zeros((num_pos, budget+1), dtype=object) # array to recreate hires

    for x in range(budget+1):
        V[num_pos-1][x] = 0
        Who[num_pos-1][x] = player()
        
        for p in players[num_pos-1]:
            # retrieve relevant players
            if p.cost <= x and p.value > V[num_pos-1][x]:
                V[num_pos-1][x] = p.value
                Who[num_pos-1][x] = p
    
    for pos in range(num_pos-2,-1,-1):
        for x in range(budget+1):
            null_player = player()
            # V[pos][x] = V[pos+1][x]     # not taking a player. we will try initializing to -inf
            V[pos][x] = 0
            Who[pos][x] = null_player

    # If it traces back the current lineup correctly the first time it should do it after that

            for p in players[pos]:
                currentTeams = {}
                currentLineup = []
                amount = x - p.cost
                for i in range(pos+1,num_pos):
                    k = Who[i][amount]
                    if type(k) != int:
                        if k.id != None:
                            if k.team in currentTeams:
                                currentTeams[k.team] += 1
                            else:
                                currentTeams[k.team] = 1
                            currentLineup.append(k.name)
                            amount = amount - k.cost
                
                if p.cost <= x and (V[pos+1][x-p.cost] + p.value >= V[pos][x]) and (p.name not in currentLineup):  # and currentTeams[p.team] < 4
                    if pos != 0:
                        if x - p.cost < 10:
                            continue
                    V[pos][x] = V[pos+1][x-p.cost] + p.value
                    Who[pos][x] = p

    return Who

# multiple lineups
def optimizeMultiple(players,budget,entries):
    """
    Returns multiple optimized lineups for either fanduel or draftkings. This function
    is provided arguments for player data, budget, and the number of entries desired.
    This function can handle up to 20 entries pretty well. It can be easily run through
    its wrapper function multipleOptimizer()
    """

    num_pos = len(players)
    lineups = []
    flineups = []
    for g in range(0,entries):
        # shuffle(players)
        V = np.zeros((num_pos, budget+1))   # array to track max vorp
        Who = np.zeros((num_pos, budget+1), dtype=object) # array to recreate hires
        for x in range(budget+1):
            V[num_pos-1][x] = 0
            Who[num_pos-1][x] = player()
            
            for p in players[num_pos-1]:
                # retrieve relevant players
                if p.cost <= x and p.value > V[num_pos-1][x]:
                    V[num_pos-1][x] = p.value
                    Who[num_pos-1][x] = p
        
        for pos in range(num_pos-2,-1,-1):
            for x in range(budget+1):
                null_player = player()
                # V[pos][x] = V[pos+1][x]     # not taking a player. we will try initializing to -inf
                V[pos][x] = 0
                Who[pos][x] = null_player

        # If it traces back the current lineup correctly the first time it should do it after that

                for p in players[pos]:
                    currentLineup = []
                    amount = x - p.cost
                    for i in range(pos+1,num_pos):
                        k = Who[i][amount]
                        if type(k) != int:
                            if k.id != None:
                                currentLineup.append(k.name)
                                amount = amount - k.cost
                    
                    if p.cost <= x and (V[pos+1][x-p.cost] + p.value >= V[pos][x]) and (p.name not in currentLineup):
                        tempCur = [p.name] + currentLineup
                        masterCopy = 0
                        fmasterCopy = 0
                        if pos != 0:
                            if x - p.cost < 10:
                                continue
                        if g > 0:
                            if pos == 5:
                                for s in lineups:
                                    diff = False
                                    for k in tempCur:
                                        if k not in s:
                                            diff = True
                                    if diff:
                                        masterCopy+=1
                                if masterCopy == len(lineups):

                                    V[pos][x] = V[pos+1][x-p.cost] + p.value
                                    Who[pos][x] = p
                            elif pos == 0:
                                for s in flineups:
                                    diff = False
                                    for k in tempCur:
                                        if k not in s:
                                            diff = True
                                    if diff:
                                        fmasterCopy+=1
                                if fmasterCopy == len(flineups):
                                    V[pos][x] = V[pos+1][x-p.cost] + p.value
                                    Who[pos][x] = p

                            else:
                                V[pos][x] = V[pos+1][x-p.cost] + p.value
                                Who[pos][x] = p
                        else:
                            V[pos][x] = V[pos+1][x-p.cost] + p.value
                            Who[pos][x] = p
                        
        names = set()
        fnames=set()
        print('-----------')
        newLineup = getLineup(Who,[],output=True)
        for p in range(4,len(newLineup)):
            names.add(newLineup[p].name)

        lineups.append(names)
        for p in range(0,len(newLineup)):
            fnames.add(newLineup[p].name)
        flineups.append(fnames)


def getLineup(Who, lockedPlayers, output=False):
    """
    Takes a 2-D array containing the solution to the Knapsack dynamic programming problem. Returns 
    a list containing the hired player objects, and optionally prints.
    """
    num_pos, budget = Who.shape
    budget -= 1 # modify since array is 1 larger than budget
    amount = budget
    points = 0
    lineup = []
    lockFlag = False

    if lockedPlayers != None and lockedPlayers != []:
        lockFlag = True

    for i in range(num_pos):
        player = None

        if lockFlag: # check if player already locked for this position, if so hire
            for p in lockedPlayers:
                if i == p[1]:   # player locked for this position
                    player = p[0]  # hire

        if player is None:   # if no player locked for this position, hire according to alg
            player = Who[i][amount]
            
        if player.id != None:
            if output: print("sign player " + str(player.name) + " for position", i, "who is projected for " + str(player.value))
            amount -= player.cost
            points += player.value
            lineup.append(player)

    if output:
        print("total money spent is " + str((budget - amount)*100))
        print("total projected points: " + str(points))
    
    return lineup

# Scrape
def scrapeNumFD():
    """
    Retrieves player projection data from NumberFire for FanDuel contests. 
    Returns 2-D array contains player objects with relevant attributes filled.
    """
    
    url = 'https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    prices = soup.findAll('td', attrs={'class':'cost'})
    names = soup.findAll('a', attrs={'class':'full'})
    teams = soup.findAll('span', attrs={'class':'team-player__team active'})
    proj = soup.findAll('td', attrs={'class':'fp active'})
    positions = soup.findAll('span', attrs={'class':'player-info--position'})
    # gtd = soup.findAll('span', attrs={'class':'team-player__injury player-gtd'})
    data = [[],[],[],[],[]]

    for i in range(0,len(prices)):
        price = int(int(re.sub('[^0-9]','', prices[i].text))/100)
        value = float(proj[i].text.strip())

        if("PG" in positions[i].text):
            data[0].append(player(value,price,i,names[i].text.strip(),teams[i].text.strip()))
        elif("SG" in positions[i].text):
            data[1].append(player(value,price,i,names[i].text.strip(),teams[i].text.strip()))
        elif("SF" in positions[i].text):
            data[2].append(player(value,price,i,names[i].text.strip(),teams[i].text.strip()))
        elif("PF" in positions[i].text):
            data[3].append(player(value,price,i,names[i].text.strip(),teams[i].text.strip()))
        elif("C" in positions[i].text):
            data[4].append(player(value,price,i,names[i].text.strip(),teams[i].text.strip()))

    return data

# Baseball scraping
def scrapeBaseFD():
    """
    Retrieves player projection data from NumberFire for FanDuel contests. 
    Returns 2-D array contains player objects with relevant attributes filled.
    """
    urlp = 'https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/pitchers'
    urlh = 'https://www.numberfire.com/mlb/daily-fantasy/daily-baseball-projections/batters'
    response = requests.get(urlh)
    soup = BeautifulSoup(response.text, "html.parser")
    prices = soup.findAll('td', attrs={'class':'cost'})
    names = soup.findAll('a', attrs={'class':'full'})
    proj = soup.findAll('td', attrs={'class':'fp active'})
    positions = soup.findAll('span', attrs={'class':'player-info--position'})
    # gtd = soup.findAll('span', attrs={'class':'team-player__injury player-gtd'})


    data = [[],[],[],[],[],[],[],[],[]]

    for i in range(0,len(prices)):
        price = int(int(re.sub('[^0-9]','', prices[i].text))/100)
        value = float(proj[i].text.strip())
        # print(names[i])

        if("C" in positions[i].text or "1B" in positions[i].text):
            data[0].append(player(value,price,i,names[i].text.strip()))
        elif("2B" in positions[i].text):
            data[1].append(player(value,price,i,names[i].text.strip()))
        elif("3B" in positions[i].text):
            data[2].append(player(value,price,i,names[i].text.strip()))
        elif("SS" in positions[i].text):
            data[3].append(player(value,price,i,names[i].text.strip()))
        elif("OF" in positions[i].text):
            data[4].append(player(value,price,i,names[i].text.strip()))
        data[5].append(player(value,price,i,names[i].text.strip()))

    # Pitchers
    response = requests.get(urlp)
    soup = BeautifulSoup(response.text, "html.parser")
    prices = soup.findAll('td', attrs={'class':'cost'})
    names = soup.findAll('a', attrs={'class':'full'})
    proj = soup.findAll('td', attrs={'class':'fp active'})
    positions = soup.findAll('span', attrs={'class':'player-info--position'})

    for i in range(0,len(prices)):
        price = int(int(re.sub('[^0-9]','', prices[i].text))/100)
        value = float(proj[i].text.strip())

        data[6].append(player(value,price,i,names[i].text.strip()))

    data2 = [data[0],data[1],data[2],data[3],data[4],data[4],data[4],data[5],data[6]]
    return data2

def scrapeGrindFD():
    """
    Retrieves player projection data from RotoGrinders for FanDuel contests. 
    Returns 2-D array contains player objects with relevant attributes filled.
    """
    #auto change by day
    url = 'https://rotogrinders.com/lineups/nba?date=' + CUR_DATE + '&site=fanduel'
    teamDict = scrapeTeams()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pts = soup.find_all('span',attrs={'class':'fpts'})
    names = soup.find_all('a',attrs={'class':'player-popup'})
    salary = soup.find_all('span',attrs={'class':'salary'})
    positions = soup.find_all('span',attrs={'class':'position'})

    data = [[],[],[],[],[]]

    for i in range(0,len(salary)):
        price = int(float(salary[i].text.replace('$','').replace('K',''))*10)
        value = float(pts[i].text.strip())
        team = 'placeholder' #teamDict[names[i].text.strip()]
        if("PG" in positions[i].text):
            data[0].append(player(value,price,i,names[i].text.strip(),team))
        elif("SG" in positions[i].text):
            data[1].append(player(value,price,i,names[i].text.strip(),team))
        elif("SF" in positions[i].text):
            data[2].append(player(value,price,i,names[i].text.strip(),team))
        elif("PF" in positions[i].text):
            data[3].append(player(value,price,i,names[i].text.strip(),team))
        elif("C" in positions[i].text):
            data[4].append(player(value,price,i,names[i].text.strip(),team))

    return data

def scrapeGrindDK():
    """
    Retrieves player projection data from RotoGrinders for FanDuel contests. 
    Returns 2-D array contains player objects with relevant attributes filled.
    """
    #auto change by day
    url = 'https://rotogrinders.com/lineups/nba?date=' + CUR_DATE + '&site=draftkings'
    teamDict = scrapeTeams()

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pts = soup.find_all('span',attrs={'class':'fpts'})
    names = soup.find_all('a',attrs={'class':'player-popup'})
    salary = soup.find_all('span',attrs={'class':'salary'})
    positions = soup.find_all('span',attrs={'class':'position'})

    data = [[],[],[],[],[],[],[],[]]

    for i in range(0,len(salary)):
        if(not str.isdigit(salary[i].text.strip().replace('$','').replace('K','').replace('.',''))):
            # print(str.isdigit(salary[i].text.strip().replace('$','').replace('K','').replace('.','')))
            continue
        price = int(float(salary[i].text.replace('$','').replace('K',''))*10)
        value = float(pts[i].text.strip())
        team = 'placeholder' # teamDict[names[i].text.strip()]
        
        if("PG" in positions[i].text):
            data[0].append(player(value,price,i,names[i].text.strip(),team))
        if("SG" in positions[i].text):
            data[1].append(player(value,price,i,names[i].text.strip(),team))
        if("SF" in positions[i].text):
            data[2].append(player(value,price,i,names[i].text.strip(),team))
        if("PF" in positions[i].text):
            data[3].append(player(value,price,i,names[i].text.strip(),team))
        if("C" in positions[i].text):
            data[4].append(player(value,price,i,names[i].text.strip(),team))
        # Guard
        if("PG" in positions[i].text or "SG" in positions[i].text):
            data[5].append(player(value,price,i,names[i].text.strip(),team))
        # Forward
        if("SF" in positions[i].text or "PF" in positions[i].text):
            data[6].append(player(value,price,i,names[i].text.strip(),team))

        # Util
        data[7].append(player(value,price,i,names[i].text.strip(),team))

    return data


def dropLock(data, dropPlayers, lockPlayers):
    """
    Checks the user has entered valid input for dropping and locking players.
    Returns an array with two elements - the first is the list of locked player objects, and the second is 
    the full list of players with dropped/locked players removed
    """
    # check user hasn't locked and dropped the same player
    commonPlayers = dropPlayers.intersection(lockPlayers)
    if commonPlayers != set():
        print('Error: You cannot lock and drop the same player(s).\nPlease remove the following player(s) from your lock/drop list:')
        for player in commonPlayers:
            print('-' + player)
        return
    
    # check players exist, find locked players and drop players
    newLockPlayers = lockPlayers.copy()
    newDropPlayers = dropPlayers.copy()
    lockObjs = []
    lockPos = []
    newData = data.copy()
    numEltsRemoved = 0
    for i in range(len(data)):
        for player in data[i]:
            if player.name in newLockPlayers:  # save lock player objects
                lockObjs.append((player, i))
                lockPos.append(i)
                newLockPlayers.remove(player.name)
                # newData.pop(i-numEltsRemoved)
                numEltsRemoved += 1
            
            elif player.name in dropPlayers:  # drop players
                newData[i].remove(player)
                newDropPlayers.remove(player.name)

    # check user hasn't supplied invalid player names
    if len(newLockPlayers) > 0 or len(newDropPlayers) > 0:
        print('Error: Unable to find the following player(s) in your drop/lock list:')
        for player in newLockPlayers:
            print('-' + player)
        for player in newDropPlayers:
            print('-' + player)
        print('Please revise and resubmit.')
        return

    # check user hasn't locked more than two players for the same position
    for i in lockPos:
        if (i < 4 and lockPos.count(i) > 2) or (i == 4 and lockPos.count(i) > 1):
            print('You have locked too many players for the same position. Please revise and resubmit.')
            return

    return [lockObjs, newData]

def formatPlayersFD(players):
    """
    Takes in a raw 2-D array of player objects by position and formats them for FanDuel contests.
    In other words, it duplicates all but the last of the inner lists, maintaining order.
    Original array: [['PG'], ['SG'], ['SF'], ['PF'], ['C']]
    Output array: [['PG'], ['PG'], ['SG'], ['SG'], ['SF'], ['SF'], ['PF'], ['PF'], ['C']]
    """
    playersNew = []
    for i in range(4):
        playersNew.append(players[i])
        playersNew.append(players[i])
    playersNew.append(players[4])
    return playersNew

# 

def scrapeTeams():
    """
    Creates a dictionary
    """ 
    url = 'https://www.numberfire.com/nba/daily-fantasy/daily-basketball-projections'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    teams = soup.findAll('span', attrs={'class':'team-player__team active'})
    names = soup.findAll('a', attrs={'class':'full'})

    teamDict = {}

    for i in range(0,len(teams)):
        name = names[i].text.strip()
        if name.count(' ') == 2:
            firstSpace = name.find(' ')
            secondSpace = name.find(' ',firstSpace+1)
            name = name[0:secondSpace]
        teamDict[name] = teams[i].text.strip()
    return teamDict


def fanduelOptimizer(system,lockPlayers, dropPlayers):
    """
    Wrapper function for optimized fanduel lineups. 
    Takes in a string argument for projection system, a set of players to lock
    and a set of players to lock. Outputs optimized fanduel lineup.

    """

    if system != "rotogrinders" and system != "numberfire":
        print("Error: 'System' arg must be either 'rotogrinders' or 'numberfire'")
        return
    if system == "numberfire":
        numberFireRawFD = scrapeNumFD()   # scrape data
        if len(numberFireRawFD[0]) == 0:
            print('Error: There are no games today. Please come back later.')
            return
        numberFireFD = formatPlayersFD(numberFireRawFD)   # format scraped data for optimizer

        x = dropLock(numberFireFD, dropPlayers, lockPlayers)  # lock/drop players
        if x != None:
            [lockedPlayers, numberFireFD] = x
            print('-----------\nOptimized Fanduel lineup for NumberFire:')
            solnNumFD = optimize(numberFireFD, 600)   # optimize lineup
            getLineup(solnNumFD, lockedPlayers, output=True)
    if system == "rotogrinders":
        grindersRawFD = scrapeGrindFD()   # scrape data
        grindersFD = formatPlayersFD(grindersRawFD)   # format scraped data for optimizer
        print(len(grindersFD))
        x = dropLock(grindersFD, dropPlayers, lockPlayers)  # lock/drop players
        if x != None:
            [lockedPlayers, grindersFD] = x
            print('-----------\nOptimized Fanduel lineup for RotoGrinders:')
            solnNumFD = optimize(grindersFD, 600)   # optimize lineup
            getLineup(solnNumFD, lockedPlayers, output=True)


def draftkingsOptimizer(system, lockPlayers, dropPlayers):
    """
    Wrapper function for optimized basketball draftkings lineups. 
    Takes in a string argument for projection system, a set of players to lock
    and a set of players to lock. Outputs optimized draftkings lineup.

    """

    if system != "rotogrinders":
        print("Error: 'System' arg must be 'rotogrinders'. Unfortunately NumberFire projections are not supported for this function yet.")
        return
    if system == "rotogrinders":
        grindersDK = scrapeGrindDK()   # scrape data

        x = dropLock(grindersDK, dropPlayers, lockPlayers)  # lock/drop players
        if x != None:
            [lockedPlayers, grindersDK] = x
            print('-----------\nOptimized DraftKings lineup for RotoGrinders:')
            solnGrindersDK = optimize(grindersDK, 500)   # optimize lineup
            getLineup(solnGrindersDK, lockedPlayers, output=True)

def baseballOptimizer(lockPlayers, dropPlayers):
    """
    Wrapper function for optimized baseball fanduel function. Function
    takes projections from numberfire.com. Function also takes inputs of sets
    for locking and dropping players.
    """
    numBase = scrapeBaseFD()
    x = dropLock(numBase, dropPlayers, lockPlayers)  # lock/drop players
    if x != None:
        [lockedPlayers, numBase] = x
        print('-----------\nOptimized FanDuel lineup for DraftKings:')
        solnBaseFD = optimize(numBase, 350)   # optimize lineup
        getLineup(solnBaseFD, lockedPlayers, output=True)


def multipleOptimizer(contest, system, entries):
    """
    Wrapper function for generating multiple lineups for basketball. Takes 
    arguments specifying contest platform, projection system, and number of lineups
    to be generated.
    """

    if contest != "draftkings" and contest != "fanduel":
        print("Error: 'contest' arg must be either 'draftkings' or 'fanduel'")
        return
    if system != "rotogrinders" and system != "numberfire":
        print("Error: 'System' arg must be either 'rotogrinders' or 'numberfire'")
        return
    if contest == "draftkings":
        if system == "numberfire":
            print("Only RotoGrinders projections are available for DraftKings optimzation.")
        grindersDK = scrapeGrindDK()
        print('-----------\nOptimized DraftKings lineups for rotoGrinders:')
        optimizeMultiple(grindersDK, 500, entries)
    if contest == "fanduel":
        if system == 'numberfire':
            grindersRawFD = scrapeNumFD()
            print('-----------\nOptimized Fanduel lineups for numberfire:')
        if system == 'rotogrinders':
            grindersRawFD = scrapeGrindFD()
        grindersFD = formatPlayersFD(grindersRawFD)
        print('-----------\nOptimized Fanduel lineups for rotoGrinders:')
        optimizeMultiple(grindersFD, 600, entries)


# won't work because of rotogrinders
# def captainShowdownOptimizer():
#     lockPlayers = set()
#     dropPlayers = set()
#     slateData = scrapeGrindDK()
#     # for slate in slateData:
#     #     x = dropLock(slate, dropPlayers, lockPlayers)    # lock/drop players
#     #     if x != None:
#     #         [lockedPlayers, grindersFD] = x
#     solnDKCaptain = optimizeDKshowdown(slateData,500)
#     getLineup(solnDKCaptain, [], output=True)

# Optimize Captain Showdown
# def optimizeDKshowdown(data,cost):
#     captains = []

#     for p in data[7]:
#         captains.append(player(int(p.value*1.5),int(p.cost*1.5),p.id,p.name))

#     showdownData = [captains,data[7],data[7],data[7],data[7],data[7]]
#     return optimizeDK(showdownData,500)


# def rotoPrices():
#     url = 'https://rotogrinders.com/projected-stats/nba-player?site=draftkings&sport=nba'

#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     outerDiv = soup.find_all('div',attrs={'class':'rgt-col'})
#     prices = outerDiv[1].find_all('div')
#     print(prices[0])

# def testAlg():
#     url = 'https://rotogrinders.com/lineups/nba?date=' + CUR_DATE + '&site=fanduel'

#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     #prices = soup.findAll('td', attrs={'class':'cost'})
#     pts = soup.find_all('span',attrs={'class':'fpts actual'})
#     names = soup.find_all('a',attrs={'class':'player-popup'})
#     salary = soup.find_all('span',attrs={'class':'salary'})
#     positions = soup.find_all('span',attrs={'class':'position'})

#     data = [[],[],[],[],[]]

#     for i in range(0,len(salary)):

#         if(i == 10 or i == 122):    # wut
#             continue
#         price = int(float(salary[i].text.replace('$','').replace('K',''))*1000)
#         value = float(pts[i].text.strip())
#         if("PG" in positions[i].text):
#             data[0].append(player(value,price,i,names[i].text.strip()))
#         elif("SG" in positions[i].text):
#             data[1].append(player(value,price,i,names[i].text.strip()))
#         elif("SF" in positions[i].text):
#             data[2].append(player(value,price,i,names[i].text.strip()))
#         elif("PF" in positions[i].text):
#             data[3].append(player(value,price,i,names[i].text.strip()))
#         elif("C" in positions[i].text):
#             data[4].append(player(value,price,i,names[i].text.strip()))

#     data2 = [data[1],data[0],data[0],data[2],data[2],data[3],data[3],data[4]]
#     optimize(data2, 56500)
# def optimizeFD(players, budget): DEPRECATED
#     """
#     Generates the optimal lineup for FanDuel based on player projections.

#     Inputs:
#         players: 2-D array containing player objects for each player by position
#         budget: amount of money to spend on players
#     """
    
#     num_pos = len(players)
    
#     V = np.zeros((num_pos, budget+1))   # array to track max vorp
#     Who = np.zeros((num_pos, budget+1), dtype=object) # array to recreate hires

#     for x in range(budget+1):
#         V[num_pos-1][x] = float("-inf")
#         Who[num_pos-1][x] = player()
        
#         for p in players[num_pos-1]:
#             # retrieve relevant players
#             if p.cost <= x and p.value > V[num_pos-1][x]:
#                 V[num_pos-1][x] = p.value
#                 Who[num_pos-1][x] = p
    
#     for pos in range(num_pos-2,-1,-1):
#         for x in range(budget+1):
#             null_player = player()
#             # V[pos][x] = V[pos+1][x]     # not taking a player. we will try initializing to -inf
#             V[pos][x] = float("-inf")
#             Who[pos][x] = null_player
            
#             for p in players[pos]:
#                 if p.cost <= x and V[pos+1][x-p.cost] + p.value > V[pos][x] and p != Who[pos+1][x-p.cost]:
#                     V[pos][x] = V[pos+1][x-p.cost] + p.value
#                     Who[pos][x] = p

#     return Who
