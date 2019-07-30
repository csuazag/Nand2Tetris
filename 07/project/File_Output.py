""" Funcion que recibe la lista con todo el codigo en assembly y crea el file.out """
def writeFile(adress, assembly):
    archivo = open(adress, 'w')
    for i in assembly:
        archivo.write(i)
    archivo.close()
    print "Success"

    
    
    
    
