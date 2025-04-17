import sys; args = sys.argv[1:]
import time
#sys.setrecursionlimit(10000)
stacks = {}
startT = time.perf_counter()
contraintSet = []
constraintDict = {}
puzzles = open(args[0]).read().splitlines()
#puzzles = ['.3548....1.4..5..9...2..5.63125.....4...9.315.7...146.9....7653..3.6...126..5897.']
symbolSet = set()
n = 9
# copied from slider 
def updateStacks(choices):
    stacks[choices] = stacks.get(choices,0)+ 1
def printBox(curr):
    return  (''.join([' '.join(curr[n*x: n*(x+1)]) + '\n' for x in range(len(curr)//n)]))

# 0 1 2 | 3 4 5 | 6 7 8 
# 9 10 11 | 4 5 6 | 7 8 9 
# 18 19 20 | 4 5 6 | 7 8 9 
#----------------------
# 27 2 3 | 4 5 6 | 7 8 9 
# 36 3 | 4 5 6 | 7 8 9 
# 45 2 3 | 4 5 6 | 7 8 9 
#-----------------------
# 54 2 3 | 4 5 6 | 7 8 9 
# 1 2 3 | 4 5 6 | 7 8 9 
# 1 2 3 | 4 5 6 | 7 8 9 

# idx squares start on: 0, 3, 6, 27, 30, 33, 54, 57, 60
def getIdxOfBox(startIdx):
    tempSet = set()
    c = startIdx
    for x in range(3):
        tempSet.add(c)
        tempSet.add(c+1)
        tempSet.add(c+2)

        c += 9
    return tempSet
def createContraintSet(n):
    for x in range(n): 
        contraintSet.append({row for row in range(x*n, x*n+n)})   
        contraintSet.append({col for col in range(x, n*n, n)}) 
    indexes = [0, 3, 6, 27, 30, 33, 54, 57, 60]
    for x in indexes:
        contraintSet.append(getIdxOfBox(x))

    for x in range(81):
        temp = set()
        for constraint in contraintSet:
            if x in constraint:
                temp.update(constraint)
        temp.remove(x)
        constraintDict.update({x : temp})

def createSymbolSet(pzl):
    tempSymbolSet = sorted([*{*pzl}])  
    tempSymbolSet.remove('.')  

    if len(tempSymbolSet) == 9:
        return tempSymbolSet

    newEle = []

    for idx in range(1, len(tempSymbolSet)):
        current = tempSymbolSet[idx-1]
        next_symbol = tempSymbolSet[idx]

        while ord(current) + 1 != ord(next_symbol):
            current = chr(ord(current) + 1)
            newEle.append(current)

    while len(tempSymbolSet) + len(newEle) < 9:
        newEle.append(chr(ord(tempSymbolSet[-1]) + len(newEle) + 1))

    return sorted(tempSymbolSet + newEle)


def isInvalid(pzl, changedIdx, idxToImposs):
    val = pzl[changedIdx]
    if val == '.':  
        return False
    if val in idxToImposs[changedIdx]:
        return True  
    return False

def isSolved(pzl):
    return '.' not in pzl


def createMORECHOICES(pzl, idxToImposs):
    bigList = []
    for idx,x in enumerate(pzl):
        if x == '.':
            bigList.append(createChoices(pzl,idx, idxToImposs) + (idx,))
            if len(bigList[-1][1]) <= 1:
                return bigList[-1][1], bigList[-1][2]
    bigList.sort()
    return bigList[0][1], bigList[0][2]

def createChoices(pzl, idx, idxToImposs):
   temp = []
   for c in symbolSet:
       wait = pzl[:idx] +  c + pzl[idx+1:]
       if not isInvalid(wait, idx, idxToImposs):
            temp.append(wait)
   return (len(temp),temp)

def updateDict(pzl, idx, dict):
    copy_dict = {k: set(v) for k, v in dict.items()}  
    val = pzl[idx]
    for affected_idx in constraintDict[idx]: 
        copy_dict[affected_idx].add(val)
    return copy_dict


def createDict(pzl):
    endDict = {}
    for key in constraintDict:
        for index in constraintDict[key]:
            if pzl[index] != '.':
                endDict.setdefault(key, set()).add(pzl[index])
        endDict.setdefault(key, set())
    return endDict

def bruteForce(pzl, idx, idxToImposs):
    if isInvalid(pzl, idx, idxToImposs): return ''
    if isSolved(pzl): return pzl

    choices, newIdx = createMORECHOICES(pzl,idxToImposs)
    #updateStacks(f"choices count {choices}")
    for subPzl in choices:
        updatedDict = updateDict(pzl, idx, idxToImposs)
        BF = bruteForce(subPzl, newIdx, updatedDict)
        if BF: return BF
    return ''

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
    
    global symbolSet
    createContraintSet(9)
    for num,curr in enumerate(puzzles):
        symbolSet = {*createSymbolSet(curr)}
        print(str(num+1)+ ": " + curr)
        impossDict  = createDict(curr)
        end = bruteForce(curr,  createMORECHOICES(curr,impossDict)[1], impossDict)
        spaces = 2 + int(len(str(num+1)))
        print((spaces * ' ') + end, end = "")
        cSum = checkSum(end)
        timer = time.perf_counter() - startT
        print(' ' +str(cSum) + ' {:.2f}s'.format(timer, 2))
        #printBox(end)

    #print(stacks.items())

profile = False
#if profile:
#    import cProfile
#    cProfile.run('main()', sort = 'tottime')
#else:
main()

#Arrush Shah, p4, 2026