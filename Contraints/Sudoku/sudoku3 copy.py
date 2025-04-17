import sys; args = sys.argv[1:]
import time
puzzles = open(args[0]).read().splitlines()

stacks = {}
startT = time.perf_counter()
contraintSet = []
constraintDict = {}
puzzles =  [".....4645..2..2......4..1..3655....."]
symbolSet = set()
n = 0
def setGlobals(newN, pzl):
    global symbolSet, n
    symbolSet = createSymbolSet(newN, pzl)
    if newN == n:
        return
    n = newN
    createContraintSet(newN)

def createSymbolSet(n, pzl):
    symbols = {*pzl}
    if '.' in symbols:
        symbols.remove('.')

    if len(symbols) < n:
        vals = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G']

        for curr in vals:
            if len(symbols) >= n: break
            if curr in symbols: continue
            symbols.add(curr)
    return symbols


def updateStacks(choices):
    stacks[choices] = stacks.get(choices, 0) + 1

def printBox(curr):
    return ''.join([' '.join(curr[n*x: n*(x+1)]) + '\n' for x in range(len(curr)//n)])

def getIdxOfBox(a, b, h, w):
    box = set()
    for r in range(h):
        for c in range(w):
            box.add((a + r) * n + (b + c))
    return box

def createContraintSet(n):
    global contraintSet, constraintDict
    contraintSet = []  
    constraintDict = {}  
    for x in range(n):
        contraintSet.append({row for row in range(x*n, x*n+n)})
        contraintSet.append({col for col in range(x, n*n, n)})

    if n == 9:
        h = w = 3
    elif n == 12:
        h, w = 3, 4
    elif n == 16:
        h = w = 4
    elif n == 6:
        h, w = 2, 3
    elif n == 15:
        h, w = 3, 5
    boxes = []
    for r in range(0, n, h):
        for c in range(0, n, w):
            block = set()
            for dr in range(h):
                for dc in range(w):
                    idx = (r + dr) * n + (c + dc)
                    block.add(idx)
            contraintSet.append(block)

    for x in range(n**2):
        temp = set()
        for constraint in contraintSet:
            if x in constraint:
                temp.update(constraint)
        temp.remove(x)
        constraintDict[x] = temp

def isInvalid(pzl, idx, symbol):
    for i in constraintDict[idx]:
        if pzl[i] == symbol:
            return True
    return False

def isSolved(pzl):
    return '.' not in pzl

def findOptimalSymbol(pzl, minCount):
    minIndexes = []
    min_symbol = None
    for cSet in contraintSet:
        symsInCSet = set(pzl[i] for i in cSet if pzl[i] != '.')
        symsNot = symbolSet - symsInCSet

        for symbol in symsNot:
            positions = []

            for idx in cSet:
                if pzl[idx] == '.' and not isInvalid(pzl, idx, symbol):
                    positions.append(idx)
            currCount = len(positions)

            if currCount < minCount:
                minCount = currCount
                minIndexes = positions
                min_symbol = symbol
                if minCount == 1:
                    break 
        if minCount == 1:
            break  
    return min_symbol, minIndexes
def createMORECHOICES(pzl):
    minCount = 10
    min_idx = -1

    for idx, cell in enumerate(pzl):
        if cell == '.':
            currCount = len(createChoices(pzl, idx))
            if currCount < minCount:
                minCount = currCount
                min_idx = idx
                if minCount <= 1:
                    return 'position', min_idx, []

    
    min_symbol, minIndexes =  findOptimalSymbol(pzl, minCount)

    if min_symbol is not None and len(minIndexes) <= minCount:
        return 'symbol', min_symbol, minIndexes
    else:
        return 'position', min_idx, []

def createChoices(pzl, idx):
    used_symbols = set(pzl[i] for i in constraintDict[idx] if pzl[i] != '.')
    return symbolSet - used_symbols

def bruteForce(pzl):
    #updateStacks("entered bruteForce")
    if isSolved(pzl):
        #updateStacks("exited through isSolved")
        return pzl

    result = ''
    choice, idxOSymbol, symPos  = createMORECHOICES(pzl)
    if choice == 'position':
        idx = idxOSymbol
        if idx == -1: return ''

        currSymbols = createChoices(pzl, idx)
        if not currSymbols:
            #updateStacks("exited through no possible symbols")
            return ''

        for symbol in currSymbols:
            if not isInvalid(pzl, idx, symbol):
                new_pzl = pzl[:idx] + symbol + pzl[idx+1:]
                result = bruteForce(new_pzl)

                if result:
                    return result

    elif choice == 'symbol':

        symbol = idxOSymbol
        positions = symPos

        for idx in positions:
            if not isInvalid(pzl, idx, symbol):

                new_pzl = pzl[:idx] + symbol + pzl[idx+1:]
                result = bruteForce(new_pzl)
                if result:
                    return result

    #updateStacks("exited through end of bruteForce")
    return result

def checkSum(pzl):
    minAscii = 127
    for c in pzl:
        if ord(c) < minAscii:
            minAscii = ord(c)
    sum = 0
    for c in pzl:
        sum += (ord(c) - minAscii)
    return sum


def main():
    global symbolSet, startT, puzzles

    
    for num, curr in enumerate(puzzles):
        print(f"{num + 1}: {curr}")
        
        n = int(len(curr)**(1/2))
        setGlobals(n, curr)
        #if len(symbolSet) < 9:
            #createSymbolSet(curr)

        #startT = time.perf_counter()

        end = bruteForce(curr)
        
        spaces = 2 + len(str(num + 1))
        
        print(f"{' ' * spaces}{end}", end="")
        
        cSum = checkSum(end)
        
        timer = time.perf_counter() - startT
        
        print(f" {cSum} {timer:.2f}s")

    #print(stacks.items())

profile = False
if profile:
    import cProfile
    cProfile.run('main()', sort='tottime')
else:
    main()

#Arrush Shah, p4, 2026




