import random

root = '1234_5678'
length = 9
width = 3
parseMe = [root, "lvl"]
seen = {root : [0,0]}

def swap(string, pos1, pos2):
    list_str = list(string)
    list_str[pos1], list_str[pos2] = list_str[pos2], list_str[pos1]
    return ''.join(list_str)

def addNodes(root, parseMe):
    idx = root.index('_')
    
    if idx - width >= 0:  # Move the blank space up
        temp = swap(root, idx, idx - width)
        if temp not in seen:
            parseMe.append(temp)
            seen[temp] = [1, 0]
        else:
            seen[root][0] += 1
            seen[temp][1] += 1

    if idx + width < length:  # Move the blank space down
        temp = swap(root, idx, idx + width)
        if temp not in seen:
            parseMe.append(temp)
            seen[temp] = [1, 0]
        else:
            seen[root][0] += 1
            seen[temp][1] += 1

    if idx % width != 0 and idx - 1 >= 0:  # Move the blank space left
        temp = swap(root, idx, idx - 1)
        if temp not in seen:
            parseMe.append(temp)
            seen[temp] = [1, 0]
        else:
            seen[root][0] += 1
            seen[temp][1] += 1

    if idx % width != width - 1 and idx + 1 < length:  # Move the blank space right
        temp = swap(root, idx, idx + 1)
        if temp not in seen:
            parseMe.append(temp)
            seen[temp] = [1, 0]
        else:
            seen[root][0] += 1
            seen[temp][1] += 1

def search(root):
    steps = 0
    count = 0
    while count < len(parseMe):
        current = parseMe[count]
        count += 1
        if current == "lvl":
            steps += 1
            parseMe.append("lvl")
            if parseMe[count] == 'lvl':
                break
        else:
            addNodes(current, parseMe)

search(root)
print(seen)
