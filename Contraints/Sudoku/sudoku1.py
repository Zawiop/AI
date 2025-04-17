import sys; args = sys.argv[1:]
import time
#sys.setrecursionlimit(10000)
contraintSet = []
constraintDict = {}
puzzles = open(args[0]).read().splitlines()
#puzzles = ['.17369825632158947958724316825437169791586432346912758289643571573291684164875293']
symbolSet = {*puzzles[0]}
symbolSet.remove('.')
n = 9
# copied from slider 
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
        temp = []
        for i in contraintSet:
            if x in i:
                temp.append(i)
        constraintDict.update({x : temp})
 
def isInvalid(pzl, idx):
    for constraint in constraintDict[idx]:
        seen = set()
        for i in constraint:
            value = pzl[i]
            if value != '.':  
                if value in seen:  
                    return True
                seen.add(value)
    return False

 
def isSolved(pzl):
    return '.' not in pzl

def createChoices(pzl):
   temp = []
   idx = pzl.find('.')
   for c in symbolSet:
       temp.append(pzl[:idx] +  c + pzl[idx+1:])
   return temp, idx

 
def bruteForce(pzl, idx):
    if isInvalid(pzl, idx): return ''
    if isSolved(pzl): return pzl
    choices, idx = createChoices(pzl)
    for subPzl in choices:
        BF = bruteForce(subPzl, idx)
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
    createContraintSet(9)
    for num,curr in enumerate(puzzles):
        startT = time.perf_counter()
        print(str(num+1)+ ": " + curr)
        end = bruteForce(curr, curr.find('.'))
        spaces = 2 + int(len(str(num+1)))
        print((spaces * ' ') + end, end = "")
        weee = checkSum(end)
        timer = time.perf_counter() - startT
        print(' ' +str(weee) + ' {:.2f}s'.format(timer, 2))


main()
#Arrush Shah, p4, 2026