import sys; args = sys.argv[1:]
import random
#import cProfile
for idx, x in enumerate(args):
    args[idx] = x.lower()
    
defPzl = '.'*27 + "ox......xo" + '.'*27
global HLLIM

oppFinder = {'o': 'x', 'x': 'o'}


directionToVal = {'N': -8, 'S': 8, 'E': 1, 'W': -1, 'NE': -7,'NW': -9,'SW': 7,'SE': 9}
def makeMove(pzl, currToken, idx, di):
    
    tokenToBeReplaced = oppFinder[currToken]
    pzlList = list(pzl)
    diVal = directionToVal[di]
    
    pzlList[idx] = currToken
    idx += diVal
    
    while pzl[idx] == tokenToBeReplaced:
        pzlList[idx] = currToken
        idx += diVal

    return ''.join(pzlList)
def checkPoss(pzl, idx, di, turn):

    mine, theirs = turn, oppFinder[turn]
    
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
    
POSSCACHE = {}
def possMoves(pzl, turn):
    if (pzl,turn) in  POSSCACHE:
        return POSSCACHE[(pzl,turn)]
    moves = []
    dirs = {}
    opp  = oppFinder[turn]
    
    for idx, val in enumerate(pzl):
        subDir = []

        if val == '.':
            for di in directionToVal:
                if  idx + directionToVal[di] <= 63 and idx + directionToVal[di] >= 0 and pzl[idx + directionToVal[di]] == opp:
                    if checkPoss(pzl, idx, di, turn):
                        moves.append(idx)
                        subDir.append(di)
                        
        dirs.update({idx:subDir})
        
    POSSCACHE[(pzl,turn)] = (moves,dirs)      
    return moves, dirs


def print2D(pzl):
    print(''.join([' '.join(pzl[8*x: 8*(x+1)]) + '\n' for x in range(len(pzl)//8)]))

def getTurn(pzl):
    val = (pzl.count('x') + pzl.count('o'))%2
    if val: return 'o'
    else: return 'x'

def convertExcel(x):
    temp = [*x]
    col = ord(temp[0]) - ord('a')
    row = int(temp[1]) - 1
    return row * 8 + col

    #print(f"Possible moves for {next}: {newIdxs}\nPreferred move: {quickMove(pzl,currIdx)}")
def print2D3(pzl, moves, idx, turn):
    toPrint2D = list(pzl)
    if idx != None: toPrint2D[idx] = turn.upper()
    if moves != None:
        for i in moves:
            toPrint2D[i] = '*'
        
    print2D(''.join(toPrint2D))
    print()
    
def runSection(pzl, currIdx, currTurn, dirs, toPrint = False):

    if toPrint: print(f'{currTurn} plays to {currIdx}')
    
    for d in dirs[currIdx]:
        pzl = makeMove(pzl, currTurn, currIdx, d)
        
    next = oppFinder[currTurn]

        
    newIdxs, newDirs = possMoves(pzl, next)
    
    newIdxs = list(set(newIdxs))
    if newIdxs == []:
        next = oppFinder[next]

            
        newIdxs, newDirs = possMoves(pzl, next)
        if newIdxs == []:
            if toPrint:
                print2D3(pzl, None, currIdx, currTurn)
                print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")
                print('No possible moves')
            return [], [], '', ''
        newIdxs = list(set(newIdxs))
     
    if toPrint:   
        print2D3(pzl, newIdxs, currIdx, currTurn)
        print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")
        print(f"Possible moves for {next}: {newIdxs}\nPreferred move: {ruleOfThumb(pzl,currTurn)}")

    return newIdxs, newDirs, pzl, next

def checkBounds(pzl, r, moves, edges, token):
    
    r = [*r]
    theirs = oppFinder[token]

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

#CHACHE = {}
def alphaBeta(brd, tkn, lwrBnd, UpperBnd):
    #if (brd, tkn) in CHACHE:
      #return CHACHE[(brd, tkn)]
    eTkn = oppFinder[tkn]
    moves, direction = possMoves(brd,tkn)
    if moves == []:
        eMoves, eDir = possMoves(brd,eTkn)
        if eMoves == []:
            temp = [brd.count(tkn) - brd.count(eTkn)]
            #CHACHE[(brd, tkn)] = temp
            return temp
        else:
            ab = alphaBeta(brd, eTkn, -UpperBnd, -lwrBnd)
            #CHACHE[(brd, tkn)] = [-ab[0]] + ab[1:] + [-1]
            
            return [-ab[0]] + ab[1:] + [-1]
        
    bestSoFar = [lwrBnd-1]
    for mv in moves:
        
        newBrd = brd
        for a in direction[mv]:
            newBrd = makeMove(newBrd, tkn, mv, a)
            
        ab = alphaBeta(newBrd, eTkn, -UpperBnd, -lwrBnd)
        score = -ab[0]
        if score < lwrBnd: continue
        if score > UpperBnd: return [score]
        if -ab[0] > bestSoFar[0]: bestSoFar = [-ab[0]] + ab[1:] + [mv]
            #CHACHE[(brd, tkn)] = bestSoFar
        lwrBnd = score + 1
    return bestSoFar

def quickMove(brd, tkn):
    if not brd: global HLLIM; HLLIM = tkn; return
    
    if brd.count('.') <= HLLIM: return alphaBeta(brd, tkn, -10000, 10000)[-1]
    return ruleOfThumb(brd, tkn)

def ruleOfThumb(brd, tkn):
    #weights = {idx : 0 for i in range(0,64)}
    # for every implement add or subtract to the weight for that idx
    moves, direction = possMoves(brd, tkn)
    #moves = [key for key,val in moves.items() if val != []]
    if moves != []:
        
       
        #if brd.count('.') < holes:
         #   moveSequence = alphaBeta(brd, tkn, -10000, 10000)
          #  return moveSequence[-1]
        
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
            turn = oppFinder[turn]

            idxs, direction = possMoves(pzl, turn)
            if idxs == []:
                print2D(pzl + '\n')
                print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")
                print("No possible moves")
                break

        if turn == 'x':
            chosen = quickMove(pzl, turn, 10)
        else:
            chosen = random.sample(possMoves(pzl, turn))
        before = pzl
        idxs, direction, pzl, turn = runSection(pzl, chosen, turn, direction, True)
        
        if idxs == []:
            return before
        

def main():
    pzl = defPzl
    turn = None
    moves = []
    runOnce = False
    
    if args == ['play']:
       ol = runGame(pzl, 'x')
       print(f'Count: {ol.count('x')} | {ol.count('o')}')
       return
    HLLIM = 5
    v = False
    if not args or args[0] == '' :
        pzl = defPzl
        moves = []
        turn = 'x'
        idxs = [26, 19, 44, 37]
        direction = {19 : ['S']}
    else:
        
        for item in args:
            if '.' in item and ('x' in item or 'o' in item):
                pzl = item
            elif item == 'v':
                v = True
            elif item == 'x' or item == 'o':
                turn = item
            elif len(item) > 5:
                moves += transcribeTranscript(item)
            elif item == 's' or item == 'S':
                # implement
                True
            elif item[:2] == 'hl':
                HLLIM = int(item[2:])
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

    idxs = list(set(idxs))
    print2D3(pzl,idxs, None, turn)
    print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")
    print(f"Possible moves for {turn}: {idxs}\n")
    print(f'My preferred move is: {ruleOfThumb(pzl, turn)}\n')
    if pzl.count('.') <= HLLIM:    
        moveSequence = alphaBeta(pzl, turn, -10000, 10000)
        print(f"Min score: {moveSequence[0]}; move sequence: {moveSequence[1:]}")
        
    newIdxs = idxs
    newDirs = direction
    ab = False
    if v:
        for index in moves:
            
            if pzl.count('.') <= HLLIM: ab = True
            newIdxs, newDirs, pzl, turn = runSection(pzl, index, turn, newDirs, True)
            
            if ab and newIdxs != []: 
                moveSequence = alphaBeta(pzl, turn, -10000, 10000)
                print(f"Min score: {moveSequence[0]}; move sequence: {moveSequence[1:]}")
                print()
                True
    else:
        for i, index in enumerate(moves):
            if i == len(moves)-1:
                newIdxs, newDirs, pzl, turn = runSection(pzl, index, turn, newDirs, True)
            else:
                newIdxs, newDirs, pzl, turn = runSection(pzl, index, turn, newDirs, False)
                
            if pzl.count('.') <= HLLIM and i == len(moves)-1 and newIdxs != []: 
                
                moveSequence = alphaBeta(pzl, turn, -10000, 10000)
                print(f"Min score: {moveSequence[0]}; move sequence: {moveSequence[1:]}")
#cProfile.run('main()', sort = 'tottime')
if __name__ == "__main__": main()

# Arrush Shah, p4, 2026
