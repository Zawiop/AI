import sys; args = sys.argv[1:]

index = int(args[0]) - 50
RE = [''] * 30

RE[20] = r"/^(?=\w*a)(?=\w*e)(?=\w*i)(?=\w*o)(?=\w*u)[a-z]+$/m"
RE[21] = r"/^([b-df-hj-np-tv-z]*[aeiou]){5}[^aeiou\s']*$/m"
RE[22] = r"/^(?=[^aeiouy]+w[^aeiou]|.+whh)[a-z]*$/m" 
RE[23] = r"/^(?!\w*[A-Z])((\w)(\w)(\w)\w*\4\3\2|(\w)(\w)\w?\6\5|(\w)\w?\7|a)$/m"
RE[24] = r"/^[ac-su-z]*(bt|tb)[ac-su-z]*$/m"
RE[25] = r"/^(?!\w*[A-Z])\w*(\w)(\1)\w*$/m"
RE[26] = r"/^\w*(\w)(\w*\1){5}\w*$/m"
RE[27] = r"/^\w*((\w)\2){3}\w*$/m"
RE[28] = r"/^\w*([^aeiou\s']\w*){13}[a-z]*$/m"
RE[29] = r"/^(?=[a-z]*$)((\w)(?!\w*\2\w*\2))*$/m"
print(RE[index])

#Arrush Shah, p4, 2026
