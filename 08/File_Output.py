def writeFile(adress,  assembly):
    archivo = open(adress, 'a')
    for i in assembly:
        archivo.write(i)
    archivo.close()
    print "Success"
    
