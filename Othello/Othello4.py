import sys; args = sys.argv[1:]
import random
for idx, x in enumerate(args):
    args[idx] = x.lower()
    
defPzl = '.'*27 + "ox......xo" + '.'*27



directionToVal = {'N': -8, 'S': 8, 'E': 1, 'W': -1, 'NE': -7,'NW': -9,'SW': 7,'SE': 9}
def makeMove(pzl, currToken, idx, di):

    if currToken == 'x':
        tokenToBeReplaced =  'o'
    else:
        tokenToBeReplaced = 'x'

    diVal = directionToVal[di]
    pzl = pzl[:idx] + currToken + pzl[idx+1:]
    idx += diVal
    while pzl[idx] == tokenToBeReplaced:
        pzl = pzl[:idx] + currToken + pzl[idx+1:]
        idx += diVal

    return pzl
def checkPoss(pzl, idx, di, turn):

    if turn == 'x':
        mine, theirs = 'x', 'o'
    else:
        mine, theirs = 'o', 'x'

    val = directionToVal[di]
    if abs(idx%8 - (idx + val)%8) > 1 or abs(idx//8 - (idx + val)//8) > 1:
            return False
    #print(idx)
    currVal = idx + val
    foundOne = False

    while True:

        if currVal < 0 or currVal > 63: # check bounds (left and right)
            return False

        piece = pzl[currVal]

        if piece == mine and foundOne: # check if there was the oppo piece, and we found a peice already
            return True
        
        elif abs(currVal%8 - (currVal + val)%8) > 1 or abs(currVal//8 - (currVal + val)//8) > 1: # check diagonal bounds
            return False
        
        elif piece == theirs: # make sure its the oppo piece, if it is continue
            foundOne = True
            currVal += val
            continue
        
        else: # if its a dot or another same peice
            return False
    
def possMoves(pzl, turn):
    moves = []
    dirs = {}
    for idx, val in enumerate(pzl):
        subDir = []

        if val == '.':
            for di in directionToVal:
                if checkPoss(pzl, idx, di, turn):
                    moves.append(idx)
                    subDir.append(di)
                    
        dirs.update({idx:subDir})
       
               
    return moves, dirs


def print2D(pzl):
    print(''.join([''.join(pzl[8*x: 8*(x+1)]) + '\n' for x in range(len(pzl)//8)]))

def getTurn(pzl):
    val = (pzl.count('x') + pzl.count('o'))%2
    if val: return 'o'
    else: return 'x'

def convertExcel(x):
    temp = [*x]
    col = ord(temp[0]) - ord('a')
    row = int(temp[1]) - 1
    return row * 8 + col

def printSection(pzl, currIdx, currTurn, dirs):

    print(f'{currTurn} plays to {currIdx}')
    for d in dirs[currIdx]:
        pzl = makeMove(pzl, currTurn, currIdx, d)
    print2D(pzl+ '\n')
    print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")
    if currTurn == 'x':
        next =  'o'
    else:
        next = 'x'
    newIdxs, newDirs = possMoves(pzl, next)
    newIdxs = list(set(newIdxs))
    if newIdxs == []:
        if next == 'x':
            next =  'o'
        else:
            next = 'x'
        newIdxs, newDirs = possMoves(pzl, next)
        if newIdxs == []:
            print('No possible moves')
            return [], [], '', ''
        newIdxs = list(set(newIdxs))
    print(f"Possible moves for {next}: {newIdxs}\n")

    return newIdxs, newDirs, pzl, next

def checkBounds(pzl, r, moves, edges, token):
    
    r = [*r]
    if token == 'x':
        theirs =  'o'
    else:
        theirs = 'x'
    for num,idx in enumerate(r):
        if pzl[idx] == '.' and idx in moves: 
            edges.append(idx)
            return 
        elif pzl[idx] == '.': break
        if pzl[idx] == token: continue
        elif pzl[idx] == theirs: 
            if num + 1 < len(r) and pzl[r[num+1]] == '.' and idx in moves:
                edges.append(idx)
                return 
            
def findSafeEdges(pzl, moves, tkn):
    safeEdges = []
    
    if pzl[0] == tkn:
        checkBounds(pzl, range(0+1,8,1), moves, safeEdges, tkn)
        checkBounds(pzl,range(0+8,64,8), moves, safeEdges, tkn)
           
    if pzl[7] == tkn:
        checkBounds(pzl,range(7-1,-1,-1), moves, safeEdges, tkn)
        checkBounds(pzl,range(7+8,64,8), moves, safeEdges, tkn)

    if pzl[56] == tkn:
       checkBounds(pzl, range(56+1,64,1), moves, safeEdges, tkn)
       checkBounds(pzl,range(54-8,-1,-8), moves, safeEdges, tkn)

    if pzl[63] == tkn:
        checkBounds(pzl, range(63-1,55,-1), moves, safeEdges, tkn)
        checkBounds(pzl, range(63-8,6,-8), moves, safeEdges, tkn)
    return safeEdges

def lookAhead(brd, tkn, moves, direction):
    if tkn == 'x':
        theirs =  'o'
    else:
        theirs = 'x'

    brdList = {}
    for idx in moves:
        new = brd
        for d in direction[idx]:
            new = makeMove(new, tkn, idx, d)
        m, no = possMoves(new,theirs)
        brdList[len(m)] = idx

    if brdList == {}: return None
    v =min(brdList)
    return (v), brdList[v]

def quickMove(brd, tkn):
    #weights = {idx : 0 for i in range(0,64)}
    # for every implement add or subtract to the weight for that idx
    moves, direction = possMoves(brd, tkn)
    #moves = [key for key,val in moves.items() if val != []]
    if moves != []:

        if 0 in moves:
            return 0
        if 7 in moves:
            return 7
        if 56 in moves:
            return 56
        if 63 in moves:
            return 63
        edges = findSafeEdges(brd, moves, tkn)
        #print(edges)
        if edges: return edges[len(edges)//2]
        for m in moves:
           if m in {18,19,20,21 ,26,29,34,37 ,42,43,44,45,46}:
               return m
        l,i =lookAhead(brd, tkn, moves, direction)
        if (l) <2: return i
        for m in moves:
            if m in {1,8,9, 6,15,14, 57,48,49, 62,55,54}:
                continue
            else: return m
        #print(moves)
        return [*{*moves}][0]
    else: return None

def transcribeTranscript(trans):
    vals = []
    for x in range(0,len(trans), 2):
        slice = trans[x:x+2]
        if '_' in slice:
            vals.append(int(slice[1]))
        else:
            vals.append(int(slice))
    return vals

def runGame(pzl, turn):
    while True:
        idxs, direction = possMoves(pzl, turn)
        
        if idxs == []:
            if turn == 'x':
                turn = 'o'
            else:
                turn = 'x'
            idxs, direction = possMoves(pzl, turn)
            if idxs == []:
                print2D(pzl + '\n')
                print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")
                print("No possible moves")
                break

        if turn == 'x':
            chosen = quickMove(pzl, turn)
        else:
            chosen = random.choice(idxs)
        before = pzl
        idxs, direction, pzl, turn = printSection(pzl, chosen, turn, direction)
        
        if idxs == []:
            return before
        

def main():
    pzl = defPzl
    turn = None
    moves = []
    runOnce = False
    #if args == ['play']:
       # ol = runGame(pzl, 'x')
        #print(f'Count: {ol.count('x')} | {ol.count('o')}')
       # return
    if not args or args[0] == '' :
        pzl = defPzl
        moves = [19]
        turn = 'x'
        idxs = [26, 19, 44, 37]
        direction = {19 : ['S']}
    else:
        for item in args:
            if '.' in item and ('x' in item or 'o' in item):
                pzl = item
            elif item == 'x' or item == 'o':
                turn = item
                runOnce = True
            elif len(item) > 50:
                moves = transcribeTranscript(item)
            elif item == 's' or item == 'S':
                # implement
                True
            else:
                moves.append(item)
        if turn == None:
            turn = getTurn(pzl)

        for i,val in enumerate(moves):
            try:
                moves[i] = int(val)
            except:
                moves[i] = convertExcel(val) 

        moves = [m for m in moves if isinstance(m, int) and m >= 0]
        idxs, direction = possMoves(pzl, turn)
        if idxs == []:
            if turn == 'x':
                next =  'o'
            else:
                next = 'x'
            newIdxs, newDirs = possMoves(pzl, next)
            if newIdxs == []:
                print2D(pzl + '\n')
                print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")
                print(f"No possible moves")
                return
            else:
                turn = next
                direction = newDirs
                idxs = newIdxs

        if not moves: moves.append(idxs[0])
        
    #print2D(pzl + '\n')
    #print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")

    print(f"Possible moves for {turn}: {idxs}\n")

    newIdxs = idxs
    newDirs = direction
    changedPzl = pzl
    printSection(changedPzl, quickMove(pzl,turn), turn, newDirs)
        

    moves, dirs = possMoves(pzl, turn)
    if moves:
        print(f"My preferred move is: {quickMove(pzl, turn)}")
    else:
        if turn == 'x':
            next =  'o'
        else:
            next = 'x'
        moves, dirs = possMoves(pzl, next)
        if moves:
            print(f"My preferred move is: {quickMove(pzl, next)}")
            
if __name__ == "__main__": main()

# Arrush Shah, p4, 2026
