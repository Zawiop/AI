import sys
sys.setrecursionlimit(5000)
CACHE = {}
def change(amt, coinList):
    if amt == 0: return 1
    if coinList == [] or amt < 0: return 0

    if (amt, tuple(coinList)) in CACHE: return CACHE[(amt, tuple(coinList))]


    val1 = change(amt - coinList[0], coinList) 
    val2 = change(amt, coinList[1:])

    CACHE[(amt, tuple(coinList))] = val1 + val2
    return val1 + val2

print(change(10000,[100,50,25,10,5,1]))