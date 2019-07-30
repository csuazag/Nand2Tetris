"""Script encargado de sacar el .asm """

def create_txt(name, binary):
    archivo = open(name, 'w')
    for i in binary:
        archivo.write("{0}\n".format(i))
    archivo.close()

def controller_file_out(name, binary):
    create_txt(name, binary)
    print ("!Success!")

