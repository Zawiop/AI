import sys; args = sys.argv[1:]
import time
args[0] = args[0].strip()
if args == []:
    args = [10]
n = 0
nInteger = False
pzl = ""
QSymbol = 'Q'
hole = '.'
filled = '~'
sys.setrecursionlimit(10000)
if args[0].isdigit():
    nInteger = True
    n = int(args[0])
    if n == 1:
        print('Q')
        print('Q')
        exit()
else:
    n = int(len(args[0]) ** 0.5)
    pzl = args[0]
    for c in pzl:
        if c != '.':
            QSymbol = c
            break
    
        
contraintSet = []
if len(args) > 1:
    QSymbol = args[1]

if hole == QSymbol or QSymbol == filled:
    QSymbol = 'Q'

if hole == filled:
    hole = '.'
    filled = '~'

# copied from slider 1
def printBox(curr):
    return  (''.join([' '.join(curr[n*x: n*(x+1)]) + '\n' for x in range(len(curr)//n)]))

def createContraintSet(n):
    for x in range(n): 
        contraintSet.append({row for row in range(x*n, x*n+n)})   
        contraintSet.append({col for col in range(x, n*n, n)})    

    for start in range(n): 
        tempSet = set()
        for i in range(start, n*n, n+1):
            tempSet.add(i)
            if (i % n) == (n - 1):   
                break
        contraintSet.append(tempSet)

    for start in range(n, n*n, n):   
        tempSet = set()
        for i in range(start, n*n, n+1):
            tempSet.add(i)
            if (i % n) == (n - 1):
                break
        contraintSet.append(tempSet)

    for start in range(n):   
        tempSet = set()
        for i in range(start, n*n, n-1):
            tempSet.add(i)
            if (i % n) == 0:   
                break
        contraintSet.append(tempSet)

    for start in range(n, n*n, n):   
        tempSet = set()
        for i in range(start + n - 1, n*n, n-1):
            tempSet.add(i)
            if (i % n) == 0:
                break
        contraintSet.append(tempSet)

 
def isInvalid(pzl):
    if pzl.count(QSymbol) < n and hole not in pzl:
        return True
    indexOfQs = [idx for idx, x in enumerate(pzl) if x ==  QSymbol]
    for contraints in contraintSet:
        count = 0
        for idx in indexOfQs:
            if idx in contraints:
                count += 1
            if count == 2:   
                return True
    return False

 
def isSolved(pzl):
    return hole not in pzl

 
def createChoices(pzl):
    holeIndex = pzl.find(hole)
    return [pzl[:holeIndex] +  QSymbol + pzl[holeIndex+1:], pzl[:holeIndex] +  filled + pzl[holeIndex+1:]]

 
def bruteForce(pzl):
    if isInvalid(pzl): return ''
    if isSolved(pzl): return pzl
    for subPzl in createChoices(pzl):
        BF = bruteForce(subPzl)
        if BF: return BF
    return ''

def main():
    startT = time.perf_counter()
    if nInteger:
        createContraintSet(n)   
        empty = ''.join([hole for o in range(n*n)])
        temp = bruteForce(empty)
    else:    
        createContraintSet(n)   
        temp = bruteForce(pzl)
        
    if temp == '':
        print("No solution")
        exit()
    temp =temp.replace(filled, hole)
    toPrint = printBox(temp)
    print(temp.replace(filled, hole) + "\n" + toPrint + 'Number of Queens in this ' + str(n) + ' by ' + str(n)  + ' puzzle is ' + str(toPrint.count(QSymbol)))
    print('In: ' + '{:.3f}s'.format(time.perf_counter() - startT, 3))

    
main()
