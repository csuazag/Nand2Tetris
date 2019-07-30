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
        matriz.append(i.split(' '))
    
    return matriz


symbols = [ 'add' ,
            'sub' ,
            'neg' ,
            'eq'  , 
            'gt'  , 
            'lt'  , 
            'and' ,
            'or'  , 
            'not' ,
            'push',
            'pop' ,
            'constant' , 
            'argument' ,
            'local'    ,
            'static',
            'that'     ,
            'this'     , 
            'temp',
            'pointer' ]



""" Funcion encargada de verificar que cada palabra reservada del codigo 
    VM este bien escrita y se encuentre en la tabla de symbols (list) """
def check_symbol(list_of_list):
    cont = 0
    for li in list_of_list:
        print li
        if len(li) == 1:
            if li[0] not in symbols:
                print ('En la linea {0}, {1} no pertenece a los symbolos del lenguaje'.format(cont, li[0]))
                return False
        else:
            if li[0] not in symbols:
                print ('En la linea {0}, {1} no pertenece a los symbolos del lenguaje'.format(cont, li[0]))
                return False
            elif li[1] not in symbols:
                print ('En la linea {0}, {1} no pertenece a los symbolos del lenguaje'.format(cont, li[1]))
                return False
            elif not li[2].isdigit():
                print ('En la linea {0}, {1} no pertenece a los symbolos numericos del lenguaje'.format(cont, li[2]))
                return False
        cont += 1
    return True



""" Funcion controladora del script que se encarga de recibir la direccion del file.asm
    y hace llamados a las funciones y luego retorna la lista con el codigo VM limpio """
def controller_file_in(file_vm):
    code = read_txt(file_vm)
    code_vm = list_to_list(code)


    if check_symbol(code_vm):
        return code_vm
    exit()
