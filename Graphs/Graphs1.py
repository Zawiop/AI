import sys; args = sys.argv[1:]
import re

dirToSym = {'ENSW' : '+', 'ENW' : '^', 'ENS' : '>' , 'ESW' : 'v', 'NSW' : '<', 'EW' : '-', 'EN' : 'L', 'NW' : 'J' , 'ES' : 'r', 'SW' : '7', 'N': 'N', 'S': 'S', 'E': 'E', 'W': 'W', 'NS' : '|', }
print(args)
def grfSize(g):
    if g: return len(g[1])
    else: return 0

def findW(size):
    height = int(size ** (1/2))
    width = size // height  
    if height * width != size:
        while True:
            width += 1
            if int(size/width) == size/width:
                return width
    return width 

def grfGProps(g):
    rwd = g[3]
    width = g[2]
    props = {'rwd': str(rwd)}
    if width is not None:
        props['width'] = width
    return props

def grfVProps(g, idx):
    if g[1][idx] != None: return {'rwd' : g[1][idx]}
    else: return {}
    

def grfNbrs(g, idx):
    if idx >= len(g[1]): return []
    return [nbr for nbr, props in g[0][idx].items() if not props.get('barrier', False)]

def grfEProps(g, num1, num2):
    
    if num2 in g[0][num1] and g[0][num1][num2]['rwd'] != None and g[0][num1][num2]['barrier'] == False: 
        return {'rwd' : g[0][num1][num2]['rwd']}
    else: return {}

def adj(v1, v2, w):
    if v1 == v2:
        return False
    row1, col1 = divmod(v1, w)
    row2, col2 = divmod(v2, w)
    return (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1)

def grfStrEdges(g):
    end = ''
    width = g[2] if g[2] else findW(len(g[1]))
    if g[2] == 0:
        return ''
    size = len(g[1])
    for idx in range(size):
        nbrs = grfNbrs(g, idx)
        dirs = ''
        for nbr in nbrs:
            if adj(idx, nbr, width):
                if nbr == idx - width:
                    dirs += 'N'
                elif nbr == idx + width:
                    dirs += 'S'
                elif nbr == idx - 1:
                    dirs += 'W'
                elif nbr == idx + 1:
                    dirs += 'E'
                else:
                    continue  # Skip jumps for visualization
        dirs = ''.join(sorted(dirs))
        end += dirToSym.get(dirs, '.')
    if end.count('.') == len(end) and g[2] == None:
        return ''
    if v := getJumps(g):
        return end + '\nJumps: ' + v
    return end

def getJumps(g):
    first = ''
    second = ''
    final = ''
    if g[5]:
        for v1,v2 in g[5]:
            first += str(v1) + ','
            second += str(v2) + ',' 
            final = first[:-1] + '~' + second[:-1]
    return final

def grfStrProps(g):
    end = ''
    end += str(grfGProps(g)) + '\n'
    for x in g[0].keys():
        val = grfVProps(g, x)
        if val:
            end += f"{x} : {val} \n"
    for v1 in g[0].keys():
        for v2 in g[0][v1].keys():
            if (v:=grfEProps(g,v1,v2)) != {}: 
                end += f"{(v1,v2)} : " + str(v) + '\n'
    return end

def handleVscle(vslc, size, width):
    arr = [*range(0, size)]
    colonCount = vslc.count(':')
    if '#' in vslc:
        nums = vslc.split('#')
        end = []
        if nums[0] == '':
            nums[0] = 0
        if nums[1] == '':
            nums[1] = size - 1
        start = int(nums[0])
        stop = int(nums[1])
        newW = (stop % width) - (start % width) + 1
        for r in range(start, stop, width):
            end += arr[r : r+newW]
        return end
    elif colonCount == 0:
        if int(vslc) > size: return []
        return [arr[int(vslc)]]
    elif colonCount == 1:
        nums = vslc.split(':')
        if nums[0] == '':
            nums[0] = 0
        if nums[1] == '':
            nums[1] = size
        return arr[int(nums[0]): int(nums[1])]
    else:
        nums = vslc.split(':')
        start = int(nums[0]) if nums[0] != '' else None
        stop = int(nums[1]) if nums[1] not in ('', None) else None
        step = int(nums[2]) if nums[2] != '' else 1
        temp = arr[start:stop:step]
        return temp

def runGraphDirective(arg):
    graph = {}
    vertexProps = {}
    size = -1
    gridWorld = True
    width = -1
    defRwd = 12    
    for idx, c in enumerate(arg):
        if c in ['G', 'N', 'W', 'R']:
            match = re.match(r'\d+', arg[idx + 1:])
            if match:
                num = int(match.group())
                if c == 'G': size = num
                elif c == 'N': gridWorld = False; size = num
                elif c == 'W': width = num
                elif c == 'R': defRwd = num
                idx += len(match.group())
            else:
                continue
    origin = width
    if width == -1 or width > size:
        width = findW(size)
    elif width == 0:
        width = findW(size)
    if gridWorld and origin != 0:
        trueWidth = width
    elif gridWorld and origin == 0:
        trueWidth = 0; gridWorld = False
    elif not gridWorld:
        trueWidth = None
    height = size//width
    for idx in range(size):
        vertexProps.update({idx : None})
        graph.update({idx : {}})
        if gridWorld:
            if idx % width > 0:
                graph[idx][idx -1] = {'rwd': None, 'barrier': False}
            if idx % width < width - 1 and idx+1 < size: 
                graph[idx][idx +1] = {'rwd': None, 'barrier': False}
            if idx//width > 0:
                graph[idx][idx - width] = {'rwd': None, 'barrier': False}
            if idx//width < height - 1 and idx+width < size:
                graph[idx][idx + width] = {'rwd': None, 'barrier': False}

    nativeEdges = {k: graph[k].copy() for k in [*graph.keys()]}
    jumps, deletedEdges = [], set()
    return [graph, vertexProps, trueWidth, defRwd, nativeEdges, jumps, deletedEdges] # ------------------------------------------------

def runVertexDirective(arg, graph):
    w = graph[2]
    if not w:
        w = findW(len(graph[1]))
    listOfVslcs = []
    terminal = False
    barrier = False
    defRwd = None
    for idx, c in enumerate(arg):
        if c in ['V', 'B', 'R', 'T']:
            if c == 'V':
                match = re.match(r'((-?\d?[:,#]-?\d?,?)|(-?\d))+', arg[idx+1:])
                listOfVslcs = match.group().split(',')
            elif c == 'T':
                terminal = True
            elif c == 'B':
                barrier = True
            else:
                #print(arg[idx+1:])
                match = re.match(r'-?\d+', arg[idx + 1:])
                if match == None: defRwd = graph[3]
                else: defRwd = int(match.group())
        else:
            continue
    allV = set()
    for x in listOfVslcs:
        allV.update({*handleVscle(x, len(graph[1]), w)})
    complement = set(graph[0].keys()) - allV
    if barrier:
        for v in allV:
            for u in graph[0][v]:
                if u in complement:
                    if not(graph[0][v][u]['barrier'] == True and isJump(v,u,w) and (v,u) not in graph[5]):
                        if u in graph[0][v]: graph[0][v][u]['barrier'] = not graph[0][v][u]['barrier']#, print(v,u,graph[0][v][u]['barrier'])
                        if v in graph[0][u]: graph[0][u][v]['barrier'] = not graph[0][u][v]['barrier']#, print(u,v,graph[0][v][u]['barrier'])

                    if (u,v) in graph[5] and graph[0][u][v]['barrier'] == True:
                        graph[5].remove((u,v))
                    if (v,u) in graph[5] and graph[0][v][u]['barrier'] == True:
                        graph[5].remove((v,u))
                    
    if defRwd != None:
        for v in allV:
            graph[1][v] = defRwd
    return graph
def isJump(v1,v2,w):
    if abs(v1-v2) > 1 and abs(v1-v2) < w or abs(v1-v2) > w or v1 == v2 or v1 % w - v2 % w > 1:
        return True
    return False
def dirToVertexes(v1s, d, w, size):
    directionToVal = {'N': -w, 'S': w, 'E': 1, 'W': -1}
    newV1s, v2s = [], []
    for vertex in v1s:
        for temp in d:
            direction = directionToVal[temp]
            candidate = vertex + direction
            if 0 <= candidate < size and adj(vertex, candidate, w):
                newV1s.append(vertex)
                v2s.append(candidate)
    return newV1s, v2s

def runEdgeDirective(arg, graph):
    management = '' 
    terminal = False
    LV1 = []
    LV2 = []
    direction = '='
    rwd = None
    E = False
    foundNews = False
    for idx, c in enumerate(arg):
        if c == 'E' and not E:
            management = arg[idx+1]
            ifMag = 2
            if management not in {'!', '+', '*', '~', '@'}:
                management = '~'
                ifMag = 1
            match = re.match(r'((-?\d?[:,#]-?\d?,?)|(-?\d))+', arg[idx+ifMag:])
            LV1 = match.group().split(',')
            idx += 1 + len(match.group())
            E = True
        elif c in {'W', 'E', 'S', 'N'} and not foundNews:
            foundNews = True
            NEWS = re.match(r'[NEWS]+', arg[idx:]).group()
            LV2 = 'NEWS'
            if '~' in arg[idx:]:
                direction = '~'
            else:
                direction = '='

        elif (c == '~' or c == '=') and management != '' and LV2 != 'NEWS':
            direction = c
            match = re.match(r'((-?\d?[:,#]-?\d?,?)|(-?\d))+', arg[idx+1:])

            if not match:
                return graph

            LV2 = match.group().split(',')
            idx += 1 + len(match.group())
            
        elif c == 'R':
            match = re.match(r'-?\d+', arg[idx + 1:])
            if not match: rwd = graph[3]
            else: rwd = int(match.group())

        elif c =='T':
            terminal = True
    if graph[2]:
        w = graph[2]
    else:
        w = findW(len(graph[1]))
    v1s = []
    for x in LV1:
        v1s += handleVscle(x, len(graph[1]), w)
    v2s = []
    if LV2 == 'NEWS':
        v1s,v2s= dirToVertexes(v1s, NEWS, w, len(graph[1]))
    else:
        for x in LV2:
            v2s += handleVscle(x, len(graph[1]), w)
    allV = zip(v1s,v2s)
    allV ={*allV}
    workedOn = set()
    for v1,v2 in allV:
        if direction == '=':
            if (v2,v1) in workedOn: continue
            workedOn.add((v1,v2))
        editEdge(v1, v2, graph, direction, management, rwd)
    return graph

def addEdge(v1,v2,g,w,rwd = None):
    graph = g[0]
    graph[v1][v2] = {'rwd': rwd, 'barrier': False}
    if v1 == v2 or not ((abs(v1 - v2) == 1 and v1 // w == v2 // w) or abs(v1 - v2) == w):
        g[5]+= [(v1,v2)]

def removeEdge(v1,v2,g,rwd = None):
    graph = g[0]
    graph[v1][v2]['barrier'] = not graph[v1][v2].get('barrier', False)

    if graph[v1][v2]['barrier'] == False and rwd != None:
        graph[v1][v2]['rwd'] = rwd

    if (v1,v2) in g[5] and graph[v1][v2]['barrier'] == True:
        g[5].remove((v1,v2))

def editEdge(v1, v2, g, direction, mag, rwd):
    graph = g[0]
    w = g[2]
    if not w:
        w = findW(len(g[1]))
    jumps = []
    if mag == '~':
        if direction == '=':  # Bidirectional
            if v2 in graph[v1]:
                removeEdge(v1,v2,g,rwd)
            else:
               addEdge(v1,v2,g,w,rwd)

            if v1 in graph[v2] and v1 != v2:
                removeEdge(v2,v1,g,rwd)
            elif v1 != v2:
                addEdge(v2,v1,g,w,rwd)

        else:  # Unidirectional

            if v2 in graph[v1]:
                removeEdge(v1,v2,g,rwd)
            else:
                addEdge(v1,v2,g,w,rwd)

    if mag == '+':
        if direction == '=':
            if v2 not in graph[v1]:
                addEdge(v1,v2,g,w,rwd)
            elif graph[v1][v2]['barrier'] == True:
                addEdge(v1,v2,g,w,rwd)

            if v1 not in graph[v2] and v1 != v2:
                addEdge(v2,v1,g,w,rwd)
            elif graph[v2][v1]['barrier'] == True:
                addEdge(v2,v1,g,w,rwd)

        else:
            if v2 not in graph[v1]:
                addEdge(v1,v2,g,w,rwd)
            elif graph[v1][v2]['barrier'] == True:
                addEdge(v1,v2,g,w,rwd)

    if mag == '!':
        
        if direction == '=':  # Bidirectional
            if v2 in graph[v1] and graph[v1][v2]['barrier'] == False:
                removeEdge(v1,v2,g)

            if v1 in graph[v2] and v1 != v2 and graph[v2][v1]['barrier'] == False:
                removeEdge(v2,v1,g)

        else:  # Unidirectional
            if v2 in graph[v1] and graph[v1][v2]['barrier'] == False:
                removeEdge(v1,v2,g)

    if mag == '*':
        if direction == '=':
            if v2 in graph[v1]:
                graph[v1][v2]['rwd'] = rwd
            if v1 in graph[v2]:
                graph[v2][v1]['rwd'] = rwd

            if v2 not in graph[v1]:
                addEdge(v1,v2,g,w,rwd)
            elif graph[v1][v2]['barrier'] == True:
                addEdge(v1,v2,g,w,rwd)

            if v1 not in graph[v2] and v1 != v2:
                addEdge(v2,v1,g,w,rwd)
            elif graph[v2][v1]['barrier'] == True:
                addEdge(v2,v1,g,w,rwd)

        else:
            if v2 in graph[v1]:
                graph[v1][v2]['rwd'] = rwd

            if v2 not in graph[v1]:
                addEdge(v1,v2,g,w,rwd)
            elif graph[v1][v2]['barrier'] == True:
                addEdge(v1,v2,g,w,rwd)
    if mag == '@':
        if direction == '=':
            if v2 in graph[v1]:
                    graph[v1][v2]['rwd'] = rwd
            if v1 in graph[v2]:
                graph[v2][v1]['rwd'] = rwd
        else:
            if v2 in graph[v1]:
                    graph[v1][v2]['rwd'] = rwd
def grfParse(lastArgs):
    graph = None
    for arg in lastArgs:
        if arg[0] == 'G':
            graph = runGraphDirective(arg)
        elif arg[0] == 'V':
            graph = runVertexDirective(arg, graph)
        elif arg[0] == 'E':
            graph = runEdgeDirective(arg, graph)
    return graph

def printBox(graph, w):
    box = graph.split('\n')
    g = box[0]
    if g == '': return ''
    end = ''
    width = findW(len(g)) if not w else int(w)
    for r in range(0, len(g), width):
        for val in range(r, r+width):
            end+= g[val]
        end += '\n'
    print(end)
    if len(box) > 1: print(box[1])

def BFS(start, graph):
    best = {}
    parseMe = []
    
    for neighbor in grfNbrs(graph, start):
        best[neighbor] = (1, {neighbor})
        parseMe.append(((start,neighbor), 1, {neighbor}))
    
    nbrsToReturn = set()    
    minDepth = None  

    while parseMe:
        node, depth, origin = parseMe.pop(0)
        prev, node = node
        if graph[1][node] is not None or (node in graph[0][prev] and graph[0][prev][node]['rwd'] != None and graph[0][prev][node]['barrier'] == False):
            if minDepth is None or depth < minDepth:
                minDepth = depth
                nbrsToReturn = set(origin)
            elif depth == minDepth:
                nbrsToReturn.update(origin)
            continue
        
        for nbr in grfNbrs(graph, node):
            if nbr not in best or depth + 1 < best[nbr][0]:
                best[nbr] = (depth + 1, set(origin))
                parseMe.append(((node,nbr), depth + 1, set(origin)))
                
            elif depth + 1 == best[nbr][0]:
                updated = best[nbr][1].union(origin)
                if updated != best[nbr][1]:
                    best[nbr] = (depth + 1, updated)
                    parseMe.append(((node,nbr), depth + 1, set(updated)))
    return nbrsToReturn

   


def policyCreater(graph):
    policy = ''
    finalJumps = []
    for index in graph[1]:
        if graph[1][index] is not None:
            policy += '*' 
            continue
        nbrs = BFS(index, graph)
        temp, jumps = createDirections(nbrs, index, graph[2], len(graph[1]))
        
        for jump in jumps:
            finalJumps.append((index, jump))
            #finalJumps.append((jump, index))
        if ''.join(sorted(temp)) == '':
            policy += '.'
            continue
        policy += dirToSym[''.join(sorted(temp))]
    return policy, finalJumps

def createDirections(nbrs, v, width, size):
    x, y = v % width, v // width
    rows = size // width

    policy = ''
    jumps = []
    nbrXY = [(nbr % width, nbr // width) for nbr in nbrs]
    
    for nx, ny in nbrXY:
        dx = nx - x
        dy = ny - y
        
        if dx == -1 and dy == 0 and nx >= 0:  # West
            policy += 'W'
        elif dx == 1 and dy == 0 and nx < width:  # East
            policy += 'E'
        elif dx == 0 and dy == -1 and ny >= 0:  # North
            policy += 'N'
        elif dx == 0 and dy == 1 and ny < rows:  # South
            policy += 'S'
        else:
            jumps.append((ny * width + nx))
            
    return policy, jumps


def main():
    graph = grfParse(args)
    edgesStr = grfStrEdges(graph)
    propsStr = grfStrProps(graph)
    print(grfNbrs(graph,14))
    printBox(edgesStr, graph[2])
    print(propsStr)
    #policy, jumps = policyCreater(graph)
    #print(f'Policy: {policy}')
    #for jump in jumps:
    #    print(f'{jump[0]}~{jump[1]};', end='')
    #print(BFS(5, graph))

if __name__ == '__main__': main()

# Arrush Shah, p4, 2026
