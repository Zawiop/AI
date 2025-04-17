args = open("test.txt", "r")
args = args.read().splitlines()
players = []
for i, a in enumerate(args): args[i] = a.strip()
for val in args: players.append(val.split())
dict = {'B' : 6,'G' : 3, 'O' : 3, 'A' : 1, 'R' : 1, 'AO' : 5, 'OB' : 10, 'BG' : 10, 'GR' : 5}

def getScores(num, players):
    scores = [0,0,0]
    for idx, player in enumerate(players):
        for point in player:
            scores[idx] += dict[point]

    print(num, end = ' ')
    scores = sorted(scores, reverse= True)
    for x in scores: print(f'{x} ', end = '')
    print()

for idx in range(0, len(players), 3):
    num = players[idx][0]
    players[idx].remove(num)
    getScores(num, players[idx:idx+3])


