import sys; args = sys.argv[1:]
import re, random, math
weightfile = open(args[0])
tranferfunc = args[1]
def T1(x):
    return x

def T2(x):
    return x if x > 0 else 0

def T3(x):
    return 1/(1+math.e**(-x))

def T4(x):
    return 2 * T3(x) - 1

def dotProduct(nodes, weights):
    return sum([nodes[i] * weights[i] for i in range(len(nodes))])
    return 1

if tranferfunc == 'T1':
    transferFunc = T1
elif tranferfunc == 'T2':
    transferFunc = T2
elif tranferfunc == 'T3':
    transferFunc = T3
elif tranferfunc == 'T4':
    transferFunc = T4
    
layerCount = 0
layersWeights = {}
nodeVals = {}
for c in weightfile:
    layersWeights[layerCount] = [float(c) for c in c.split(' ')]
    nodeVals[layerCount] = ['' for _ in range(len(layersWeights[layerCount]))]
    layerCount += 1
nodeVals[0] = [float(val) for val in args[2:]]

countofnodes = [len(list(layersWeights.values())[-1])]
counter = 1
for layerList in list(layersWeights.values())[-2::-1]:
    countofnodes.append(len(layerList)//countofnodes[counter-1])
    counter +=1
countofnodes= countofnodes[::-1]
currNodes = nodeVals[0]
print(layersWeights)

for layer, count in enumerate(countofnodes):
    weights = layersWeights[layer]
    if layer == len(countofnodes)-1:
        currNodes = [node * weight for node, weight in zip(currNodes, weights)]
        break

    temp = [] 
    for i in range(countofnodes[layer+1]):
        weightTemp = weights[i * len(currNodes):(i+1) * len(currNodes)]
        temp.append(transferFunc(dotProduct(currNodes, weightTemp)))
    currNodes = temp

print(currNodes) 
# Arrush Shah, p4, 2026