import sys; args = sys.argv[1:]
import random
import time
#import cProfile
t = time.perf_counter()
args = ['test.txt']
puzzles = open(args[0]).read().splitlines()
startT = time.perf_counter()
goal = puzzles[0]
length = len(goal)
width = int(length ** (1 / 2))
goalPosMod = {char: idx%4 for idx, char in enumerate(goal)}
goalPosDivide = {char : idx//4 for idx, char in enumerate(goal)}

print(len(goal))
def FChange(pzl1, pzl2, idxNew, blank_idx):
    manPzl1 = abs(idxNew % width - goalPosMod.get(pzl1[idxNew])) + abs(idxNew // width -goalPosDivide.get(pzl1[idxNew]))
    manPzl2 = abs(blank_idx % width - goalPosMod.get(pzl2[blank_idx])) + abs(blank_idx // width -goalPosDivide.get(pzl2[blank_idx]))
    return manPzl2 - manPzl1

def isSolvable(root, goal):
    inversions = inversionCount(root, goal)
    blank_row = (root.index('_') // width) - goal.index('_')//width
    
    if inversions % 2 == blank_row % 2:
        return True
    else:
        return False

def manDistance(pzl1):
    distance = 0
    for idx, x in enumerate(pzl1):
        if x == '_':  
            continue
        distance += abs(idx % width - goalPosMod.get(x))
        distance += abs(idx // width -goalPosDivide.get(x))
    
    return distance

def inversionCount(root, goal):
    root = root.replace('_', '')
    goal = goal.replace('_', '')
    ic = 0
    for idx, x in enumerate(root):
        for y in root[idx + 1:]:
            if goal.index(x) > goal.index(y):
                ic += 1
    return ic

def swap(s, pos1, pos2):
    lst = [*s]
    lst[pos1], lst[pos2] = lst[pos2], lst[pos1]
    return ''.join(lst)

def printer(root, closedSet):
    toPrint = []
    current = closedSet.get(root)
    while current[2] != 'G':
        toPrint.append(current[2])
        current = closedSet.get(current[0])
    return toPrint[::-1]

def addNodes(root):
    toReturn = []
    idx = root.index('_')
    if idx - width >= 0:  # Up
        temp = swap(root, idx, idx - width)
        toReturn.append((temp, 'U', idx-width))
    if idx + width < length:  # Down
        temp = swap(root, idx, idx + width)
        toReturn.append((temp, 'D', idx +width))
    if (w:=idx % width) != 0 and idx - 1 >= 0:  # Left
        temp = swap(root, idx, idx - 1)
        toReturn.append((temp, 'L', idx-1))
    if w != width - 1 and idx + 1 < length:  # Right
        temp = swap(root, idx, idx + 1)
        toReturn.append((temp, 'R', idx+1))
    return idx,toReturn


def insert(newF, openSet, nbr):
    for idx, val in enumerate(openSet):
        if newF < val[0]: 
            openSet.insert(idx, (newF, nbr))
            return True
    return False

def aStar(root, goal, count):
    
    prevNodeTracker = {}
    prevNodeTracker[root] = (root, 0, 'G') 
    
    if not isSolvable(root, goal):
        print(str(count) + ": " + root + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": X")
        return None
    openSet= []
    for x in range(105):
        openSet.append([])
    openSet[manDistance(root) + 1] = [root]  # (f, pzl)
    closedSet = {}  
    lowestBucket = manDistance(root) +1
    counterInBucket = 0
    while openSet:
        if len(openSet[lowestBucket]) <= counterInBucket:
            lowestBucket +=2
            counterInBucket = 0
        curr = openSet[lowestBucket][counterInBucket]
        counterInBucket +=1
        currPzl = curr

        if currPzl in closedSet:
            continue

        closedSet[currPzl] = prevNodeTracker[currPzl][1] + 1
        
        if currPzl == goal:
            print(str(count) + ": " + root + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": " + ''.join(printer(currPzl, prevNodeTracker)))
            break

        idxBlank,nodes = addNodes(currPzl)

        for nbr in nodes:
            if nbr[0] not in closedSet:
                if nbr[0] not in closedSet:
                    temp = 110
                else:
                    temp = closedSet.get(nbr[0])

                if nbr[0] not in prevNodeTracker or temp > closedSet[currPzl] + 1:
                    prevNodeTracker[nbr[0]] = (currPzl, closedSet[currPzl], nbr[1])

                   # newF = prevNodeTracker[nbr[0]][1] + manDistance(nbr[0]) + 1
                    TestnewF =  lowestBucket +  FChange(currPzl ,nbr[0], nbr[2], idxBlank) + 1
                    #print(str(newF) + "  " + str(TestnewF))
                    openSet[TestnewF].append(nbr[0])
def main():
    c = 1
    for x in puzzles:
        if x == goal:
            print(str(c) + ": " + x + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": G")
        else:
            aStar(x, goal, c)
        c += 1
main()
#cProfile.run('main()', sort = 'tottime')
#Arrush Shah, p4, 2026