import sys; args = sys.argv[1:]

index = int(args[0]) - 30
RE = [''] * 30

RE[20] = r"/\w*(\w)\w*\1\w*/i"
RE[21] = r"/\w*(\w)\w*(\1\w*){3}/i"
RE[22] = r"/^[01]$|^([01])[01]*\1$/" 
RE[23] = r"/\b(?=\w*cat)\w{6}\b/i"
RE[24] = r"/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i"
RE[25] = r"/\b(?!\w*cat)\w{6}\b/i"
RE[26] = r"/\b((\w)(?!\w*\2))+\b/i"
RE[27] = r"/(?!.*10011)^[01]*$/"
RE[28] = r"/\w*([aeiou])(?!\1)[aeiou]\w*/i"
RE[29] = r"/^(1(?!01|11)|0)*$/"
print(RE[index])

#Arrush Shah, p4, 2026