"""Script encargado de recibir un archivo .asm, guardar todo el codigo
   en una lista, cada elementos de la lista es una linea de codigo sin espacios
   en blanco y sin comentarios. """


"""Funcion encargada de lectura de fichero, retorna una lista con todas 
   las lineas del codigo en assembly exceptuando las lineas en blanco, 
   espacios en blanco saltos de linea al fina de la cadenal"""
def read_txt(file_asm):
    file = open(file_asm, 'r')
    lines = file.readlines()
    code = []
    for i in lines:
        i = i.rstrip() #Quita espacios en blanco y \n al final del str
        if len(i) != 0: 
            code.append(i)
    return code


"""Funcion encargada de quitar todos los espacios en blanco y los comentarios"""
def clean_txt(code):
    new_code = []
    for i in code:
        i = i.replace(' ', '') #Quitando espacios en blanco        
        index = i.find('/')    #Si tiene comentarios encontrar el index del /
        if index != -1: 
            i = i[:index]
        if len(i) != 0:
            new_code.append(i)
    return new_code
         

""" Funcion controladora del script que se encarga de recibir la direccion del file.asm
    y hace llamados a las funciones read_txt() y clean_txt(), luego retorna la lista con
    el codigo assembly limpio """
def controller_file_in(file_asm):
    code = read_txt(file_asm)
    code = clean_txt(code)
    return code
