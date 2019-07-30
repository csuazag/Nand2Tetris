"""Funcion encargada de lectura de fichero, retorna una lista con todas 
   las lineas del codigo en VM exceptuando las lineas en blanco, saltos
   de linea al fina de la cadenal y quitando los comentarios /"""
def read_txt(file_vm):
    file = open(file_vm, 'r')
    lines = file.readlines()
    code = []

    for i in lines:
        
        i = i.rstrip('\n')
        i = i.rstrip('\r')
        
        index = i.find('/')

        if index != -1:
            i = i[:index]
        
        if len(i) != 0:
            code.append(i)
    return code



""" Funcion encargada de convertir en lista de listas todas las instrucciones en codigo VM,
    cada instruccion se convierte en una lista y se agrega a la lista externa """
def list_to_list(code):
    matriz = []
    for i in code:
        matriz.append(i.split())    
    return matriz


""" Funcion encargada de retornarme el codigo VM en lista de listas y retornarme la cantidad de push static
    encuentra en este fichero para reservar el espacio en la memoria.
"""
def count_push_static(code):
    count_static = 0
    for i in code:
        if i[0] == 'push' and i[1] == 'static':
            count_static += 1

  
    return code, count_static


""" Funcion controladora del script que se encarga de recibir la direccion del file.asm
    y hace llamados a las funciones y luego retorna la lista con el codigo VM limpio """
def controller_file_in(file_vm):
    code = read_txt(file_vm)
    code =  list_to_list(code)
    
    return count_push_static(code)

