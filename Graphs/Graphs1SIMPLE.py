import sys; args = sys.argv[1:]
import re

dirToSym = {'ENSW' : '+', 'ENW' : '^', 'ENS' : '>' , 'ESW' : 'v', 'NSW' : '<', 'EW' : '-', 'EN' : 'L', 'NW' : 'J' , 'ES' : 'r', 'SW' : '7', 'N': 'N', 'S': 'S', 'E': 'E', 'W': 'W', 'NS' : '|', }
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
    rwd = g[1][0]
    width = g[2]
    props = {'rwd': str(rwd)}
    if width is not None:
        props['width'] = width
    return props

def grfVProps(g, idx):
    
    return {idx : {'rwd' : g[1][idx]}}

def grfNbrs(g, idx):
    if idx >= len(g[1]): return []

    return g[0][idx].keys()

def grfEProps(g, num1, num2):
    return {}
    
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
            if nbr == idx - width:
                dirs += 'N'
            elif nbr == idx + width:
                dirs += 'S'
            elif nbr == idx - 1:
                dirs += 'W'
            elif nbr == idx + 1:
                dirs += 'E'
        dirs = ''.join(sorted(dirs))
        # Map directions to characters
        end += dirToSym.get(dirs, '.')
    if end.count('.') == len(end): return ''

    return end


def grfStrProps(g):
    end = ''
    end += str(grfGProps(g)) + '\n'
    for x in g[0].keys():
        val = grfVProps(g, x)
        end += f" {x}: {val} \n"
    
    return end


def handleVscle(vslc, size, width):
    arr = range(0, size)
    colonCount = vslc.count(':')
    if '#' in vslc:
        # Your existing code for '#' handling remains unchanged.
        nums = vslc.split('#')
        end = []
        if nums[0] == '':
            nums[0] = 0
        if nums[1] == '':
            nums[1] = size - 1

        for r in range(int(nums[0]), int(nums[1]), width):
            for val in range(r, r + (int(nums[1]) % width) + 1):
                end.append(arr[val])
        return end

    elif colonCount == 0:
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
        
        if nums[2] == '':
            nums[2] = '1'
        step = int(nums[2])

        if nums[0] == '':
            nums[0] = str(size-1) if step < 0 else '0'
        if nums[1] == '':
            nums[1] = '0' if step < 0 else str(size)
        return set([*arr[int(nums[0]): int(nums[1]): int(nums[2])]])

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

    if gridWorld and origin != 0: trueWidth = width
    elif gridWorld and origin == 0: trueWidth = 0; gridWorld = False
    elif not gridWorld: trueWidth = None

    height = size//width
    for idx in range(size):
        vertexProps.update({idx : defRwd})
        graph.update({idx : set()})
        if gridWorld:
            if idx % width > 0:
                graph[idx].add(idx - 1)

            if idx % width < width - 1 and idx+1 < size: 
                graph[idx].add(idx + 1)

            if idx//width > 0:
                graph[idx].add(idx - width)

            if idx//width < height - 1 and idx+width < size:
                graph[idx].add(idx + width)
    nativeEdges = graph.copy()
    return [graph, vertexProps, trueWidth, defRwd, nativeEdges]

def runVertexDirective(arg, graph):
    listOfVslcs = []
    terminal = False
    barrier = False
    defRwd = graph[3]
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
                match = re.match(r'-?\d+', arg[idx + 1:])
                defRwd = int(match.group())
        else:
            continue
    allV = set()
    for x in listOfVslcs:
        allV.update({*handleVscle(x, len(graph[1]), findW(len(graph[1])))})

    complement = set(graph[0].keys()) - allV
    nativeEdges = graph[4]
    if barrier:
        for v in allV: # every vertex specified
            for u in graph[0][v]: # for all the edges
                if u in complement: 
                   graph[0][v].discard(u)
                   graph[0][u].discard(u)

        for v in allV:
            for u in nativeEdges[v]:
                if u in complement and u not in graph[0][v]:
                    graph[0][v].add(nativeEdges[v][u])
                    graph[0][u].add(nativeEdges[u][v])
    for v in allV:
        for u in graph[0][v]:
             graph[0][v][u] = defRwd
             graph[0][u][v] = defRwd
    return graph
def runEdgeDirective (arg):
    return
# data struct - {vertex : [other vertices]} (list refers to nbrs)
def grfParse(lastArgs):
    for arg in lastArgs:
        if arg[0] == 'G':
            graph = runGraphDirective(arg)
            #printBox(grfStrEdges(graph), graph[2])
        elif arg[0] == 'V':

            graph = runVertexDirective(arg, graph)

            # vertex directive
        elif arg[0] == 'E':
            graph = runEdgeDirective(arg)

            # edge directive
        
  
    return graph
def printBox(g, w):
    if g == '': return ''
    end = ''
    width = findW(len(g)) if not w else int(w)
    for r in range(0, len(g), width):
        for val in range(r, r+width):
            end+= g[val]
        end += '\n'
    print(end)

def main():
    graph = grfParse(args)
    #print(graph)
    #print(grfGProps(graph))
    print(grfNbrs(graph, 7))
    edgesStr = grfStrEdges(graph)
    propsStr = grfStrProps(graph)
    printBox(edgesStr, graph[2])
    print(propsStr)

if __name__ == '__main__': main()

#Arrush Shah, p4, 2026