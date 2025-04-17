import sys; args = sys.argv[1:]

index = int(args[0]) - 30
RE = [''] * 10
RE[0] = r"/^0$|^10[01]$/"
RE[1] = r"/^[01]*$/"
RE[2] = r"/0$/"
RE[3] = r"/\w*[aeiou]\w*[aeiou]\w*/i"
RE[4] = r"/^0$|^1[01]*0$/"
RE[5] = r"/^[01]*110[01]*$/"
RE[6] = r"/^.{2,4}$/s"
RE[7] = r"/^\d{3} *-? *\d\d *-? *\d{4}$/"
RE[8] = r"/^.*?d\w*/im"
RE[9] = r"/^[01]?$|^0[01]*0$|^1[01]*1$/"
print(RE[index])


#Arrush Shah, p4, 2026