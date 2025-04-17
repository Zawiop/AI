import sys; args = sys.argv[1:]
#import math
import random
import time
#import re
t = time.perf_counter()

root = 0
goal = 0
length = 0
width = 0
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

def printer(steps, current, detSeen):
    toPrint = [current]
    current = detSeen[current]
    while current != root:
        if(current != 'lvl'):
            toPrint.append(current)
            current= detSeen[current]
    toPrint.append(current)

    for x in range(len(toPrint)):
        toPrint[x] = printBox(toPrint[x])

    for x in range(len(toPrint)//8 + 1):
        printBand(toPrint[::-1][8*x:], 8)
        print("\n")
    print("Steps: " + str(steps) + "\nTime: ", end = " ")

def printBox(curr):
    return  (''.join(['-'.join(curr[width*x: width*(x+1)]) + '\n' for x in range(len(curr)//width)]))

def printBand(curr, bandLength):
    box = []
    for x in range(bandLength):
        if(len(curr) <= x):
            break
        temp = curr[x]
        box.extend(temp.split('\n'))
    for x in range(width):
        print(' '.join(box[x::width+1]))
        
def addNodes(root, parseMe, seen):
    if((idx := root.index('_')) - width >= 0): # bottom
        temp =swap(root, idx, idx-width)
        if(temp not in seen):
            parseMe.append(temp)
            seen.update({temp : root})
        
    if(idx + width < length ): # top
        temp = swap(root, idx, idx+width)
        if(temp not in seen):
            parseMe.append(temp)
            seen.update({temp : root})

    if(idx % width != 0 and idx -1 >= 0): # left
        temp = swap(root, idx, idx-1)
        if(temp not in seen):
            parseMe.append(temp)
            seen.update({temp : root})

    if(idx % width != width-1 and idx +1 < length): # right
        temp =swap(root, idx, idx+1)
        if(temp not in seen):
            parseMe.append(temp)
            seen.update({temp : root})

def search(root, goal, print):
    parseMe = [root, "lvl"]
    detSeen = {root : root}
    steps = 0
    count = 0
    while parseMe:
        current = parseMe[count]
        count +=1
        if(current == "lvl"):
            steps +=1
            parseMe.append("lvl")
            if(parseMe[count] == 'lvl'):
                break
        else:
            if(current == goal):
                if(print):
                    printer(steps, current, detSeen)
                else:
                    return steps
                break

            addNodes(current, parseMe, detSeen)

def regRun():     
    if(root == goal):
            print(printBox(root))
            print("Steps: 0\nTime: ", end = " ")
    elif(width == 3 and inversionCount(root,goal) % 2 == 1):
        print(printBox(root))
        print("Steps: -1\nTime: ", end = " ")

    else:
        search(root, goal, True)
if(not args):
    pzls = 500
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
    root = args[0]
    length = len(root)
    width = int(length **0.5) 
    if(len(args) > 1):
        goal = args[1]
    else:
        goal = ''.join(sorted(root.replace('_', ''))) + "_"
    regRun()

timer = time.perf_counter() - t
print('{:.2f}s'.format(timer, 2) + "\nAvgTime per Pzl: " + '{:.4f}s'.format(timer/numSolvable, 4))

#Arrush Shah, p4, 2026