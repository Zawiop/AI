import sys; args = sys.argv[1:]
import random
import time
import cProfile

class pq:
    def __init__(self):
        self.myList = []

    def add(self, val):
        self.myList.append(val); self.myList.sort(reverse = True)
    def min(self):
        self.myList[-1]
    def RMin(self):
        self.myList.pop(0)
    def max(self):
        self.myList[0]
    def RMax(self):
        self.myList.pop(0)
t = time.perf_counter()
# args = ['test.txt']
puzzles = open(args[0]).read().splitlines()

goal = puzzles[0]
length = len(goal)
width = int(length ** (1 / 2))


def isSolvable(root, goal):
    inversions = inversionCount(root, goal)
    blank_row = (root.index('_') // width)
    if (inversions + blank_row % 2)%2 == 1:
        return True
    else:
        return False

def manDistance(pzl1, pzl2):
    pos = {char: idx for idx, char in enumerate(pzl2)}
    distance = 0
    for idx, x in enumerate(pzl1):
        if x == '_':  
            continue
        distance += abs(idx % width - pos.get(x) % width)
        distance += abs(idx // width - pos.get(x) // width)
    
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
        toReturn.append((temp, 'U'))
    if idx + width < length:  # Down
        temp = swap(root, idx, idx + width)
        toReturn.append((temp, 'D'))
    if idx % width != 0 and idx - 1 >= 0:  # Left
        temp = swap(root, idx, idx - 1)
        toReturn.append((temp, 'L'))
    if idx % width != width - 1 and idx + 1 < length:  # Right
        temp = swap(root, idx, idx + 1)
        toReturn.append((temp, 'R'))
    return toReturn

def insert(newF, openSet, nbr):
    for idx, val in enumerate(openSet):
        if newF < val[0]: 
            openSet.insert(idx, (newF, nbr))
            return True
    return False

def aStar(root, goal, count):
    t = time.perf_counter()
    prevNodeTracker = {}
    prevNodeTracker[root] = (root, 0, 'G') 
    
    if not isSolvable(root, goal):
        print(str(count) + ": " + root + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": X")
        return None

    openSet = [(manDistance(root, goal) + 1, root)] # (f, pzl)
    closedSet = {}  
    backCount = 0
    while openSet:

        curr = openSet.pop(0)
        backCount +=1
        currPzl = curr[1]

        if currPzl in closedSet:
            continue

        closedSet[currPzl] = prevNodeTracker[currPzl][1] + 1
        
        if currPzl == goal:
            print(str(count) + ": " + root + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": " + ''.join(printer(currPzl, prevNodeTracker)))
            break

        nodes = addNodes(currPzl)
        for nbr in nodes:
            if nbr[0] not in closedSet:
                if nbr[0] not in closedSet:
                    temp = 1000000
                else:
                    temp = closedSet.get(nbr[0])

                if nbr[0] not in prevNodeTracker or temp > closedSet[currPzl] + 1:
                    prevNodeTracker[nbr[0]] = (currPzl, closedSet[currPzl], nbr[1])

                    newF = prevNodeTracker[nbr[0]][1] + manDistance(nbr[0], goal) + 1
                    
                    inserted = insert(newF, openSet, nbr[0])

                    if not inserted:
                        openSet.append((newF, nbr[0]))

def main():
    c = 1
    for x in puzzles:
        if x == goal:
            print(str(c) + ": " + x + " in " + '{:.2f}s'.format((time.perf_counter() - t), 2) + ": G")
        else:
            aStar(x, goal, c)
        c += 1
cProfile.run('main()', sort = 'tottime')

#Arrush Shah, p4, 2026