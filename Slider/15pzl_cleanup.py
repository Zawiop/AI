import sys; args = sys.argv[1:]
import time
#import cProfile

width = 4

def aStar(initial, goal):
    if not inversion_count(initial, goal):
        return ''
    frontier = [[] for i in range(105)]
    goaldict = {let:x for x, let in enumerate(goal)}
    tcost = manhattan(initial, goaldict)
    #print(tcost)
    frontier[tcost].append((initial,[initial]))
    explored = {initial:tcost}
    for i, bucket in enumerate(frontier):
        for cur in bucket:
            node = cur[0]
            if node == goal:
                path = get_path(cur[1])
                return path
            index, childs = generate_children(node)
            #print(childs)
            for childList in childs:
                child = childList[0]

                # if time.time() - start > 3:
                #    return 0, ''
                totalcost = i + fchange(node, child, goaldict, index, childList[1])
                if child not in explored or explored[child] > totalcost:
                    #print(cur[1], child, totalcost, manhattan(child, goaldict))
                    explored[child] = totalcost
                    temp = cur[1][:]
                    temp.append(child)
                    frontier[totalcost].append((child, temp))
    return 0, ''

def get_path(pl):
    path = ''
    zipstuff = zip(pl, pl[1:])
    for first, second in zipstuff:
        if width == (firstind := first.index('_')) - (secondind := second.index('_')):
            path += 'U'
        elif -1*width == firstind - secondind:
            path += 'D'
        elif 1 == firstind - secondind:
            path += 'L'
        elif -1 == firstind - secondind:
            path += 'R'
    return path

def swap(state, i, j):
    if i > j:
        i, j = j, i
    return state[:i] + state[j] + state[i+1:j] + state[i] + state[j+1:]

def generate_children(initial):
    childlist = []
    index = initial.index('_')
    swaplist = swapindex[index]
    for each in swaplist:
        childlist.append((swap(initial, index, each), each))
    return index, childlist

def inversion_count(state,goal):
    odd = True
    sinitial = state.index('_')
    ginitial = goal.index('_')
    if ((ginitial // width) % 2) == ((sinitial // width) % 2):
        odd = False
    if goal == state:
        return 0
    state = state.replace('_', '')
    goal = goal.replace('_', '')
    count = 0
    for i in range(len(state)):
        index = goal.index(state[i])
        for j in range(i+1, len(goal)):
            if index > goal.index(state[j]):
                count += 1
    if (odd and count % 2 == 1) or ((not odd) and count % 2 == 0):
        return True
    return False

def manhattan(initial, goaldict):
    count = 0
    for index, i in enumerate(initial):
        if i != '_':
            initialind = index
            goalind = goaldict[i]
            count += abs((initialind // 4) - (goalind // 4))
            count += abs((initialind % 4) - (goalind % 4))
    return count

def fchange(cur, child, goaldict, indexch, indexcur):
    uno = abs(indexcur // 4 - goaldict[cur[indexcur]] // 4)
    dos = abs(indexcur % 4 - goaldict[cur[indexcur]] % 4)
    tres = abs(indexch // 4 - goaldict[child[indexch]] // 4)
    quatro = abs(indexch % 4 - goaldict[child[indexch]] % 4)
    if uno + dos > tres + quatro:
        return 0
    return 2

def starter():
    start = time.time()
    for i, pzl in enumerate(puzzles):
        print(str(i) + ": " + pzl, end = ' ')
        if(pzl == goal):
            print('G')
        else:
            path = aStar(pzl, goal)
            if path == '':
                print('X')
            else:
                print('len ' + str(len(path)) + ' in ' + '{:.2f}s'.format(time.time()-start, 2) + ': ' + path)
                start = time.time()

puzzles = open(args[0]).read().splitlines()
goal = puzzles[0]
#goal = 'KAEDOFCLNGMB_IHJ'
#puzzles = ['AOJDKFBE_ICMLNGH']
goaldict = {let:x for x, let in enumerate(goal)}
swapindex = {0:[1,4], 1:[0,2,5], 2:[1,3,6], 3:[2,7], 4:[0,5,8], 5:[1,4,6,9], 6:[2,5,7,10], 7:[3,6,11], 8:[4,9,12], 9:[5,8,10,13], 10:[6,9,11,14], 11:[7,10,15], 12:[8,13], 13:[9,12,14], 14:[10,13,15], 15:[11,14]}
start = time.time()
starter()
#cProfile.run('starter()', sort = 'tottime')

# Suraj Kidiyoor, 5, 2026