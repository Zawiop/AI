myStr = '012345678'
w = 3

print('\n'.join(([myStr[x:x+w] for x in range(0,len(myStr),w)])))

#temp = [v for v in lst for lst in lstOflsts]