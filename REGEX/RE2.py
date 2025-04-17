import sys; args = sys.argv[1:]

index = int(args[0]) - 30
RE = [''] * 20

RE[10] = r"/^[x.o]{64}$/i"
RE[11] = r"/^[xo]*\.[xo]*$/i"
RE[12] = r"/^\.|\.$|^(x*o*\.+o*x+|x+o*\.+o*x*)$/i"
RE[13] = r"/^.(..)*$/s"
RE[14] = r"/^((0|1[01])([01]{2})*)$/"
RE[15] = r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i"
RE[16] = r"/^(1?0)*1*$/"
RE[17] = r"/^[bc]*a[bc]*$|^[bc]+$/"
RE[18] = r"/^([bc]*(a[bc]*){2})+$|^[bc]+$/"
RE[19] = r"/^(2[20]*|(1[20]*){2})+$/"
print(RE[index])

r"-?(\d\d\d,?).\d*"
#Arrush Shah, p4, 2026