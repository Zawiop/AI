myStr = '0123456789'
w = 3

print('\n'.join*[[myStr[x] for x in range(w *y, y* w +w)] for y in range(0,len(myStr)//w)])