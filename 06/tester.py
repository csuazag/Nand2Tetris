"""Script para probar mi salida .hack y la salida .hack del Assembler.sh """

l1 = raw_input("Ingrese direccion 1")
l2 = raw_input("Ingrese direccion 2")

archive1 = open(l1, 'r')
info1  = archive1.readlines()
print info1

print ""

archive2 = open(l2, 'r')
info2 = archive2.readlines()
print info2

if info1 == info2:
    print "MELO ESTRELLA DE KLEEN"
else:
    print "FALLA"


x = len(info1)
y = len(info2)

if x == y:
    x = 0
    while x < len(info1):
        if info1[x] != info2[x]:
            print "Falle en {0}".format(x)
            exit()
        x+=1
else:
    print "No tienen la misma longitud"
