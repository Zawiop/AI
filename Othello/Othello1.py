import sys; args = sys.argv[1:]
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

def main():
    pzl = defPzl
    turn = None
    moves = []
    if not args or args[0] == '' :
        pzl = defPzl
        moves = [19]
        turn = 'x'
        idxs = [26, 19, 44, 37]
        direction = {19 : ['S']}
    else:
        for item in args:
            if len(item) == 64:
                pzl = item
            elif item == 'x' or item == 'o':
                turn = item
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
        
    print2D(pzl + '\n')
    print(pzl + f" {pzl.count('x')}/{pzl.count('o')}")

    print(f"Possible moves for {turn}: {idxs}\n")

    newIdxs = idxs
    newDirs = direction

    for index in moves:
        newIdxs, newDirs, pzl, turn = printSection(pzl, index, turn, newDirs)


if __name__ == "__main__": main()

# Arrush Shah, p4, 2026
