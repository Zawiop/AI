import sys; args = sys.argv[1:]
# Arrush Shah, p4, 2026

import random
#import cProfile
import time
for idx, x in enumerate(args):
    args[idx] = x.lower()
    
defPzl = '.'*27 + "ox......xo" + '.'*27
global HLLIM, MIDGAMEDEPTH
HLLIM = 8
MIDGAMEDEPTH = 4
starttime = time.perf_counter()
oppFinder = {'o': 'x', 'x': 'o'}

directionToVal = {'N': -8, 'S': 8, 'E': 1, 'W': -1, 'NE': -7,'NW': -9,'SW': 7,'SE': 9}
newNEWS = {'N':  (0, -1),'S':  (0,  1),'E':  (1,  0),'W':  (-1, 0),'NE': (1, -1),'NW': (-1, -1),'SE': (1,  1),'SW': (-1, 1)}


LINES = {}
for idx in range(64):
    row, col = divmod(idx, 8)
    for di, (dx, dy) in newNEWS.items():
        line = []
        r, c = row, col
        while True:
            r += dy
            c += dx
            if not (0 <= r < 8 and 0 <= c < 8):
                break
            line.append(r * 8 + c)
        LINES[(idx, di)] = line
        
        


class Strategy:
    # Uncomment the below flags as needed
    # logging = True
    # uses_10x10_board = True
    # uses_10x10_moves = True

    def best_strategy(self, board, player, best_move, still_running, time_limit):
        best_move.value = ruleOfThumb(board, player)
        best_move.value = quickMove(board, player)


def getOpeningMove(pzl, turn):
   
    if turn != 'o':
        return None
    
    xC = pzl.count('x')
    oC = pzl.count('o')
    
    if xC + oC > 6:
        return None

    if xC == 3 and oC == 2:
        xsMove = None
        for i in range(64):
            if pzl[i] == 'x' and defPzl[i] == '.' and idx != 19 and idx != 26 and idx != 37 and idx != 44:
                xsMove = i
                break

        responses = {
            19: 26,
            26: 19,
            37: 44,
            44: 37
        }
        
        if xsMove in responses:
            return responses[xsMove]
        else:
            return None
    
    return None

MAKEMOVECACHE = {}
def makeMove(pzl, currToken, idx, di):
    if (pzl,currToken,idx,di) in MAKEMOVECACHE:
        return MAKEMOVECACHE[(pzl,currToken,idx,di)]
    tokenToBeReplaced = oppFinder[currToken]
    pzlList = list(pzl)
    diVal = directionToVal[di]
    
    pzlList[idx] = currToken
    idx += diVal
    
    while pzl[idx] == tokenToBeReplaced:
        pzlList[idx] = currToken
        idx += diVal

    MAKEMOVECACHE[(pzl,currToken,idx,di)] = (w:=''.join(pzlList))
    return w

def checkPoss(pzl, idx, di, turn):
    mine, theirs = turn, oppFinder[turn]
    line = LINES[(idx, di)]
    if not line:
        return False
    
    if pzl[line[0]] != theirs:
        return False
    
    for cell in line[1:]:
        if pzl[cell] == theirs:
            continue
        
        elif pzl[cell] == mine:
            return True
        
        else:  
            return False
    return False
    
POSSCACHE = {}
def possMoves(pzl, turn):
    if (pzl, turn) in POSSCACHE:
        return POSSCACHE[(pzl, turn)]
    moves = []
    dirs = {}
    opp = oppFinder[turn]
    for idx in range(64):
        if pzl[idx] != '.':
            dirs[idx] = []
            continue
        subDir = []
        for di in directionToVal:  
            line = LINES[(idx, di)]
            if not line:
                continue
            if pzl[line[0]] == opp and checkPoss(pzl, idx, di, turn):
                subDir.append(di)
        if subDir:
            moves.append(idx)
        dirs[idx] = subDir
    POSSCACHE[(pzl, turn)] = (moves, dirs)
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
        print(f"Possible moves for {next}: {newIdxs}\nPreferred move: {quickMove(pzl,currTurn)}")

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

def addUpBounds(pzl, r, token):
    
    r = [*r]
    count= 0
    for num,idx in enumerate(r):
        if pzl[idx] == token: 
            count += 1
        elif pzl[idx] == '.': break
        if pzl[idx] == token: continue
    return count
            
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

def brdEval(brd, tkn):
    return brdEvalOneSided(brd, tkn) - brdEvalOneSided(brd, oppFinder[tkn])


def corners(brd, tkn):
    
    #print (t)
    return 1 * (brd[0] == tkn) + 1 * (brd[7] == tkn) + 1 * (brd[56] == tkn) + 1 * (brd[63] == tkn)

def safeEdgesIn(brd, tkn):
    count = 0
    if brd[0] == tkn:
        count += (w:=addUpBounds(brd, range(0+1,8,1),tkn))
        if w < 7: count += addUpBounds(brd,range(0+8,64,8), tkn)
           
    if brd[7] == tkn:
        count += (w:=addUpBounds(brd,range(7-1,-1,-1),  tkn))
        if w < 7: count += addUpBounds(brd,range(7+8,64,8),tkn)

    if brd[56] == tkn:
       count += (w:=addUpBounds(brd, range(56+1,64,1),  tkn))
       if w < 7:count += addUpBounds(brd,range(54-8,-1,-8),tkn)

    if brd[63] == tkn:
        count += (w:=addUpBounds(brd, range(63-1,55,-1),tkn))
        if w < 7:count += addUpBounds(brd, range(63-8,6,-8), tkn)
    return count

def brdEvalOneSided(brd, tkn):
    #cornerWeight = 1000
    #safeEdgeWeight = 1
    #numMovesWeight = 100
    #tokenWeight = 1/100
    # Corners + Edges (Weights) ~ 82%
    #val = corners(brd, tkn) * cornerWeight + safeEdgeWeight * safeEdgesIn(brd, tkn)
    
    # PossMoves + Corners ~ 84%
    #val = corners(brd, tkn) * cornerWeight + len(possMoves(brd,tkn)[0])  * numMovesWeight - brd.count(tkn) * tokenWeight
    
    # Moblity
    #player_moves = len(possMoves(brd,tkn)[0])
    #opponent_moves = len(possMoves(brd,oppFinder[tkn])[0])
    #val = 100 * (player_moves - opponent_moves) / (player_moves + opponent_moves)
    
    # Counting our tokens and opponent tokens and scaling it from -100 to 100
    ourTkns = brd.count(tkn)
    oppTkns = brd.count(oppFinder[tkn])

    coinParity = 100.0 * (ourTkns - oppTkns) / (ourTkns + oppTkns)
    
    # Counting possibile moves of us and our opponnent, scaling it from -100 to 100
    playerMoves = len(possMoves(brd,tkn)[0])
    oppMoves = len(possMoves(brd,oppFinder[tkn])[0])
    if oppMoves == 0: # Checking if opponent has no possible moves, this is the best move always
        return 100
    mobility = 0.0
    if playerMoves + oppMoves > 0: # Checking if both players have possible moves
        mobility = 100.0 * (playerMoves - oppMoves) / (playerMoves + oppMoves)
    
    # Counting  # of corners of us and our opponnent, scaling it from -100 to 100
    playerCorners = corners(brd, tkn)
    oppCorners = corners(brd, oppFinder[tkn])
    cornerValue = 0.0
    if playerCorners + oppCorners > 0: # Checking if corners exist to avoid divide by zero
        cornerValue = 100.0 * (playerCorners - oppCorners) / (playerCorners + oppCorners)
        
    # Counting  # of stable edges of us and our opponnent, scaling it from -100 to 100
    playerStable = safeEdgesIn(brd, tkn)
    oppStable = safeEdgesIn(brd, oppFinder[tkn])
    stability = 0.0
    if playerStable + oppStable > 0: # Avoiding /0
        stability = 100.0 * (playerStable - oppStable) / (playerStable + oppStable)
    
    # Weights for all four values 
    tknWeight = 0.05
    mobilityWeight = 0.3
    cornerWeight = 0.45
    stabilityWeight = 0.2
    # Val is between -100 to 100
    val = tknWeight * coinParity + mobilityWeight * mobility + cornerWeight * cornerValue + stabilityWeight * stability
    return val

MIDCACHE = {}

def order(moves, brd, tkn):
    
    corners = {0, 7, 56, 63}
    edges = set(range(8)) | set(range(56, 64)) 
    edges = set(range(0, 64, 8)) | set(range(7, 64, 8))  

    def move_priority(m):
        if m in corners:
            return 0   
        elif m in edges:
            return 1
        else:
            return 2

    return sorted(moves, key=move_priority)

def midgameAB(brd, tkn, lwrBnd, UpperBnd, depth):
    
    if depth >= MIDGAMEDEPTH:
        return [brdEval(brd, tkn)]
    
    eTkn = oppFinder[tkn]
    moves, direction = possMoves(brd,tkn)
    if moves == []:
        #eMoves, eDir = possMoves(brd,eTkn)
        #if eMoves != []:
            #temp = [brd.count(tkn) - brd.count(eTkn)]
            #CHACHE[(brd, tkn)] = temp
            #return temp
        
            ab = midgameAB(brd, eTkn, -UpperBnd, -lwrBnd, depth + 1)
            #CHACHE[(brd, tkn)] = [-ab[0]] + ab[1:] + [-1]
            
            return [-ab[0]] + ab[1:] + [-1]
    
    ordered = order(moves, brd, tkn)
    bestSoFar = [lwrBnd-1]
    for mv in ordered:
        
        newBrd = brd
        for a in direction[mv]:
            newBrd = makeMove(newBrd, tkn, mv, a)
            
        ab = midgameAB(newBrd, eTkn, -UpperBnd, -lwrBnd, depth + 1)
        score = -ab[0]
        if score < lwrBnd: continue
        if score > UpperBnd: return [score]
        if -ab[0] > bestSoFar[0]: bestSoFar = [-ab[0]] + ab[1:] + [mv]
            #CHACHE[(brd, tkn)] = bestSoFar
        lwrBnd = score + 1
    return bestSoFar


def quickMove(brd, tkn):
    if not brd: global HLLIM; HLLIM = tkn; return
    
    if brd.count('.') <= HLLIM: 
        return alphaBeta(brd, tkn, -100000, 100000)[-1]
    #print(f'Preferred move: {ruleOfThumb(brd,tkn)}')
    START_AB = time.time()
    return midgameAB(brd, tkn, -100000, 100000, 0)[-1]

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

def runGame(pzl, turn, yourToken):
    transcript = []
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

        if turn == yourToken:
            chosen = quickMove(pzl, turn)
        else:
            moves, dict = possMoves(pzl, turn)
            chosen = random.choice([*moves])
        before = pzl
        trans = '0' + f'{chosen}' if len(f'{chosen}') < 2 else f'{chosen}'
        transcript.append(trans)
        idxs, direction, pzl, turn = runSection(pzl, chosen, turn, direction, False)
        
        if idxs == []:
            return before, transcript
        
def clearCaches():
    global POSSCACHE
    POSSCACHE = {}
    global MAKEMOVECACHE
    MAKEMOVECACHE = {}
    
def main():
    
    pzl = defPzl
    turn = None
    moves = []
    runOnce = False
    global HLLIM, MIDGAMEDEPTH
    if args[0][0] == 'p':
       games = 5
       if len(args[0]) > 1:
           games = int(args[0][1:])
       avgs = []
       countOfLost = 0
       tkn = 'x'
       scoreToPzl = {}

       for i in range(games):
           
            if i == games//2:
                tkn = 'x'
                print('Flipped Symbol')
                
            pzl = defPzl
            ol, trans = runGame(pzl, tkn, tkn)
            score = round(((ol.count(tkn)*100)/(ol.count('x') + ol.count('o'))), 2)
            scoreToPzl[score] = (ol, trans)
            if ol.count(tkn) == 0:
                print(f'Game {i+1} done, you got skunked', flush= True)
            elif ol.count(oppFinder[tkn]) == 0:
                print(f'Game {i+1} done, you skunked them', flush= True)
            elif ol.count(tkn) > ol.count(oppFinder[tkn]):
                    avgs.append(score)
                    print(f'Game {i+1} won: {score}%', flush= True)
                #print(print2D(ol))
            else:
                print(f'Game {i+1} lost -------')
                countOfLost +=1
            clearCaches()
            avgs.append( score)
            
            
       print()
       print(f'Average scores: {round(sum(avgs)/len(avgs),2)}%')
       flukes = max(games//10, 1)
       avgsWithoutFluke = avgs
       #for a in range(flukes):
        #   print(f'Fluke: {(w:=round(avgsWithoutFluke.pop(avgsWithoutFluke.index(min(avgsWithoutFluke))), 2))}')
        #   print(f'{print2D(scoreToPzl[w][0])}\n{''.join(scoreToPzl[w][1])}')
           
       #print(f'Average scores without fluke: {round(sum(avgsWithoutFluke)/len(avgsWithoutFluke), 2)}%')
       #print(f'Number of flukes counted: {flukes}')
       print(f'Time: { round(time.perf_counter() - starttime, 2)}s')
       print(f'HLLIM: {HLLIM}')
       print(f'Depth: {MIDGAMEDEPTH}')
       
   
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
            next = oppFinder[turn]
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
    #print(f"My preferred move is: {ruleOfThumb(pzl, turn)}\n")
    if turn == 'o' and 64 - pzl.count('.') < 30:
        print(f'My preferred move is: {ruleOfThumb(pzl, turn)}\n')
    else:
        if pzl.count('.') <= HLLIM:    
            moveSequence = alphaBeta(pzl, turn, -100000, 100000)
            print(f"Min score: {moveSequence[0]}; move sequence: {moveSequence[1:]}")
        else: 
            moveSequence = midgameAB(pzl, turn, -100000, 100000, 0)
            print(f"Min score: {moveSequence[0]}; move sequence: {moveSequence[1:]}")
        print(f'My preferred move is: {moveSequence[-1]}\n')

    
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

