import sys; args = sys.argv[1:]
import time

def readInput(args):
    pieces = []
    for arg in args:
        
        arg = arg.replace('X', 'x')
        if 'x' in arg:
            parts = arg.split('x')
            pieces.extend(parts)
        else:
            pieces.append(arg) # pieces are just nums, ordered in w, h, w, h etc
    
    pieces = [int(token) for token in pieces]
    boxHeight, boxWidth = pieces[0], pieces[1]
    blocks = []
    idx = 2
    while idx < len(pieces):
        if idx + 1 < len(pieces):
            h, w = pieces[idx], pieces[idx + 1]
            blocks.append({'h': h, 'w': w, 'placed': False})
            idx += 2
        else:
            break
    return boxHeight, boxWidth, blocks # getting blocks

def placeable(block, space):
    return block['h'] <= space['h'] and block['w'] <= space['w']

def findNewSpace(space, block): #calcuations for the new dimensions of the space remaining
    newSpace = []
    
    if block['w'] < space['w']:
        spaceRight = {'x': space['x'] + block['w'], 'y': space['y'], 'h': block['h'], 'w': space['w'] - block['w']}
        newSpace.append(spaceRight)
    
    if block['h'] < space['h']:
        spaceDown = {'x': space['x'], 'y': space['y'] + block['h'], 'h': space['h'] - block['h'], 'w': space['w']}
        newSpace.append(spaceDown)
    
    if block['w'] < space['w'] and block['h'] < space['h']:
        spaceNot = {'x': space['x'] + block['w'], 'y': space['y'] + block['h'], 'h': space['h'] - block['h'], 'w': space['w'] - block['w']}
        newSpace.append(spaceNot)
    return newSpace

def sortBlocks(blocks):
     return sorted(blocks, key=multiply, reverse=True)

def multiply(b):
    return b['h'] * b['w']

def getValues(b):
    return b['y'], b['x']

def solved(blocksRemaining):
    if all(block['placed'] for block in blocksRemaining):
        return True

def bruteForce(freeSpace, blocksRemaining, blocksPlaced, impossibles):
    
            
    p1 = tuple(sorted([(space['x'], space['y'], space['h'], space['w']) for space in freeSpace])) # creating a list of all the space thats open 
    p2 = tuple(sorted([block['placed'] for block in blocksRemaining])) # list of all the blocks reamining
    if (p1,p2) in impossibles: # improvement 6
        return None
    impossibles[(p1,p2)] = True

    if solved(blocksRemaining): # if solved
        return blocksPlaced

    
    blocksRemaining = sortBlocks(blocksRemaining)

    for block in blocksRemaining: # for all blocks
        if block['placed']: # if its placed why iterate through the spots
            continue
        for i, space in enumerate(freeSpace): # free space indexes

            for orientation in ['original', 'rotated']: # each orientation 

                if orientation == 'rotated':
                    block['h'], block['w'] = block['w'], block['h']

                if placeable(block, space): # if the block can be placed in that index
                    
                    newBlock = {'x': space['x'], 'y': space['y'], 'h': block['h'], 'w': block['w']}
                    block['placed'] = True
                    currPlacedBlocks = blocksPlaced + [newBlock]
                    
                    newSpace = freeSpace[:i] + freeSpace[i+1:]
                    temp = findNewSpace(space, block)
                    newSpace.extend(temp)
                    
                    result = bruteForce(newSpace, blocksRemaining, currPlacedBlocks, impossibles) # recur again
                    if result is not None:
                        return result
                    
                    block['placed'] = False
                
                if orientation == 'rotated':
                    block['h'], block['w'] = block['w'], block['h']
    return None

def printer(blocks,h,w):
    
    blocks.sort(key=getValues)
    dimensions = []
    ones = ""
    for block in blocks:
        dimensions.append(f"{block['h']}x{block['w']}")
    for x in range(findTotalArea(blocks), w*h):
        ones += "1x1 "
    return ones  + ' '.join(dimensions)

def findTotalArea(blocks):
    totalArea = 0
    for x in blocks:
        totalArea += x['h'] * x['w']
    return totalArea
def main():
    boxHeight, boxWidth, blocks = readInput(args)
    ST = time.perf_counter()
    freeSpace = [{'x': 0, 'y': 0, 'h': boxHeight, 'w': boxWidth}]
    blocksPlaced = []
    impossibles = {}
    result = bruteForce(freeSpace, blocks, blocksPlaced, impossibles)
    ET = time.perf_counter()
    if result is not None and findTotalArea(blocks) <= boxHeight * boxWidth:
        output = printer(result,boxHeight,boxWidth)
        print("Decomposition:", output)
        print("Time taken: {:.2f}s".format(ET - ST))
    else:
        print("No solution")

main()



#Steps

# grab biggest block, and place it where it can be placed excluding rotational repeats
# for each instance of new puzzle recur again and place the next biggest block, 
# repeat above until all blocks are placed

# improvements
# if the open area is bigger than the area of leftover blocks, return

#Arrush Shah, p4, 2026
