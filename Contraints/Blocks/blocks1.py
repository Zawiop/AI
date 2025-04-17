import sys; args = sys.argv[1:]
import time
puzzles = []
box = ()

def findArea(puzzles):
    area = 0
    for p in puzzles:
        ints = p.split('X')
        area += int(ints[0]) * int(ints[1])
    return area

if 'X' in args[0] or 'x' in args[0]:
    box = args[0]
    box = box.upper()
    args = args[1:]
else:
    box = (args[0], args[1])
    args = args[2:]
added = False

for num, t in enumerate(args):
    if added:
        added = False
        continue
    if 'X' in t or 'x' in t:
        t = t.upper()
        puzzles.append(t)
    else:
        puzzles.append(t + 'X' + args[num+1])
        added = True
print(findArea(puzzles))
boxDim = box.split('X')
if len(puzzles) > 1 and findArea(puzzles) < int(boxDim[0]) * int(boxDim[1]):
    print('Decomposition: ' + ' '.join(puzzles))
elif box == puzzles[0]:
    print("Decomposition: " + puzzles[0])
else: 
    print('No solution')


#Arrush Shah, p4, 2026


#Steps

# grab biggest block, and place it where it can be placed excluding rotational repeats
# for each instance of new puzzle recur again and place the next biggest block, 
# repeat above until all blocks are placed

# improvements
# if the open area is bigger than the area of leftover blocks, return
