import sys; args = sys.argv[1:]
import random
import time
import cProfile
t = time.perf_counter()
#args = ['test.txt']
puzzles = open(args[0]).read().splitlines()
startT = time.perf_counter()
goal = puzzles[0]
length = len(goal)
width = int(length ** (1 / 2))

goalPosMod = {char: idx%4 for idx, char in enumerate(goal)}
goalPosDivide = {char : idx//4 for idx, char in enumerate(goal)}

def FChange(pzl2, blank_idx):
    manPzl2 = abs(blank_idx % width - goalPosMod.get(pzl2[blank_idx])) + abs(blank_idx // width -goalPosDivide.get(pzl2[blank_idx]))
    return manPzl2

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
    root = root.replace('_', '',1)
    goal = goal.replace('_', '', 1)
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

def printer2(root, closedSet):
    path = []
    curr = goal
    while curr != root:
        path.append({1: 'R', -1: 'L', -4: 'U', 4 : 'D'}[curr.index('_')- closedSet[curr].index('_')])
        curr = closedSet[curr]
    return path[::-1]

def addNodes(root):
    toReturn = []
    idx = root.index('_')
    if idx - width >= 0:  # Up
        temp = swap(root, idx, idx - width)
        toReturn.append((temp, idx-width))

    if idx + width < length:  # Down
        temp = swap(root, idx, idx + width)
        toReturn.append((temp, idx +width))

    if (w:=idx % width) != 0 and idx - 1 >= 0:  # Left
        temp = swap(root, idx, idx - 1)
        toReturn.append((temp, idx-1))
        
    if w != width - 1 and idx + 1 < length:  # Right
        temp = swap(root, idx, idx + 1)
        toReturn.append((temp, idx+1))
    return idx,toReturn

def aStar(root, goal):
    t = time.perf_counter()
    openSet = [[] for x in range(105)]
    openSet[manDistance(root)] = [(root,root)]  # f -> curr, prev
    closedSet = {}  

    for lowestBucket, bucket in enumerate (openSet):
        for currPzl, prev in bucket:
            if time.perf_counter() -  t > 6.0:
                return None

            if currPzl in closedSet:
                continue
            
            closedSet[currPzl] = (prev) # pzl -> prev
            if currPzl == goal:
                return closedSet

            idxBlank,nodes = addNodes(currPzl)

            for nbr in nodes:
                # newF  = prevNodeTracker[nbr[0]][1] + manDistance(nbr[0]) + 1
                currInfo =  abs(nbr[1] % width - goalPosMod.get(currPzl[nbr[1]])) + abs(nbr[1] // width -goalPosDivide.get(currPzl[nbr[1]]))
                TestnewF =  lowestBucket +  FChange(nbr[0], idxBlank) + 1 - currInfo
                openSet[TestnewF].append((nbr[0], currPzl))
def main():
    for c, x in enumerate(puzzles):
        if x == goal:
            print(str(c) + ": " + x + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": G")
        elif not isSolvable(x, goal):
            print(str(c) + ": " + x + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": X")
        else:   
            closedSet = aStar(x, goal)
            if closedSet:
                print(str(c) + ": " + x + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": " + ''.join(printer2(x, closedSet)))
            else:
                print(str(c) + ": " + x + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": X")

#main()
cProfile.run('main()', sort = 'tottime')
#Arrush Shah, p4, 2026