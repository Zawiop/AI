import sys; args = sys.argv[1:]
#import math
import random
import time
#import re
t = time.perf_counter()
#args = ['test.txt']
puzzles = open(args[0]).read().splitlines()

goal = puzzles[0]
length = len(goal)
width = int(length**(1/2))

def manDistance(pzl1, pzl2):
    pzl1 = pzl1.replace('_','') 
    pzl2 = pzl2.replace('_', '')
    distance = 0 
    for idx,x in enumerate(pzl1):
        distance += abs(idx%width - (temp := pzl2.index(x))%width)
        print(str(idx) + " "  + str(temp))

         
    return distance

def inversionCount(root, goal):
    root = root.replace('_','') 
    goal = goal.replace('_', '')
    ic = 0
    for idx,x in enumerate(root):
       for y in root[idx+1:]:
            if(goal.index(x) > goal.index(y)):
                ic += 1
    return ic

def swap(str ,pos1, pos2):
    list = [*str]
    list[pos1], list[pos2] = list[pos2], list[pos1]
    str = ''.join(list)
    return str

def printer(current, detSeen):
    toPrint = []
    current = detSeen[current]
    while current[0] != root:
        if(current != 'lvl'):
            toPrint.append(current[1])
            current= detSeen[current[0]]
    
    toPrint.append(current[1])
    return toPrint[::-1]
    
def addNodes(root, parseMe, seen):
    if((idx := root.index('_')) - width >= 0): # bottom
        temp =swap(root, idx, idx-width)
        if(temp not in seen):
            parseMe.append(temp)
            seen.update({temp : (root, "U")})
    if(idx + width < length ): # top
        temp = swap(root, idx, idx+width)
        if(temp not in seen):
            parseMe.append(temp)
            seen.update({temp : (root, "D")})

    if(idx % width != 0 and idx -1 >= 0): # left
        temp = swap(root, idx, idx-1)
        if(temp not in seen):
            parseMe.append(temp)
            seen.update({temp : (root, "L")})

    if(idx % width != width-1 and idx +1 < length): # right
        temp =swap(root, idx, idx+1)
        if(temp not in seen):
            parseMe.append(temp)
            seen.update({temp : (root, "R")})

def search(root, goal, print):
    parseMe = [root, "lvl"]
    detSeen = {root : (root, 'NA')}
    steps = 0
    count = 0
    while parseMe:
        current = parseMe[count]
        count +=1
        if(current == "lvl"):
            steps +=1
            parseMe.append("lvl")
            if(parseMe[count] == 'lvl'):
                return ["X"]
        else:
            if(current == goal):
                if(print):
                    return printer(current, detSeen)
                else:
                    return steps
                
            addNodes(current, parseMe, detSeen)

def regRun(root, count):     
    if(root == goal):
            print(str(count) + ": " + root + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": G")
    elif(width == 3 and inversionCount(root,goal) % 2 == 1):
            print(str(count) + ": " + root + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": X")
    else:
        path = search(root, goal, True)
        print(str(count) + ": " + root + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": " + ''.join(path))
        
if(not args):
    pzls = 20
    length = 9
    width = 3
    avgSteps = 0
    numSolvable = 0
    goal = '12345678_'
    for x in range(pzls):
        root = ''.join(random.sample([*goal], 9))
        if(inversionCount(root, goal) % 2 != 1):
            avgSteps += search(root, goal, False)
            numSolvable += 1
        if(x% 10 == 0):
            print('*', end = '', flush= True)
    print('\nPzls: '+ str(pzls) +'\n' + 'Solvable: ' + str(numSolvable) + '\navgSteps: ' + str(avgSteps//numSolvable) +  "\nTime: ", end = " " )
else:
    count = 0
    for root in puzzles:
        count+= 1
        regRun(root, count)

timer = time.perf_counter() - t
#print('{:.2f}s'.format(timer, 2) + "\nAvgTime per Pzl: " + '{:.4f}s'.format(timer/numSolvable, 4))

#Arrush Shah, p4, 2026