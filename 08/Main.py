import sys, shutil
import File_Input
import Translator
import File_Output
#Import para leer ficheros en la carpeta
from os import listdir



def main():
    bandera = True
    puntero_static_anterior = 0
    puntero_stack_anterior  = 0

    cant_static_file = []

    direccion_carpeta = sys.argv[1]

    separacion = direccion_carpeta.split('/')
    a = -1

    ruta_carpeta = ''
    nombre_fichero = ''
    nombre_carpeta = ''

    while a >= (-len(separacion)):
        if separacion[a] != '':
            if separacion[a].find('.vm') != -1:
                k = separacion[a]
                nombre_fichero = k[:-3] + '.asm'
                separacion.pop()
                break
            else:                          
                nombre_carpeta = separacion[a] + '.asm'
                break
        a -= 1

    
    for i in separacion:
        ruta_carpeta += i + '/'       



 
    files = []
    for i in listdir(ruta_carpeta):
        if i.find('.vm') != -1: files.append(i)
    

    if len(files) == 0:
        print 'No encontre ningun archivo .vm'
        

    existe_sysvm = False
    if 'Sys.vm' in files:
        files.remove('Sys.vm')
        files.insert(0, 'Sys.vm')
        existe_sysvm = True
    print files


    nombre_fichero_salida = ''
    if len(nombre_fichero) != 0:                
        nombre_fichero_salida = ruta_carpeta + nombre_fichero        
    else:
        nombre_fichero_salida = ruta_carpeta + nombre_carpeta
        
    archivo = open(nombre_fichero_salida, 'w')
    archivo.close()


   
    for file_name in files:
        
        tupla_entrada = File_Input.controller_file_in(ruta_carpeta+file_name)

        code_vm     = tupla_entrada[0]
        cant_static = tupla_entrada[1]
        


        if bandera: 
            tupla_traductor = Translator.controller_translation(existe_sysvm, i, code_vm)
            bandera = False            
        else:
            tupla_traductor = Translator.controller_translation(existe_sysvm, i, code_vm, puntero_stack_anterior, puntero_static_anterior)


        code_assembly          = tupla_traductor[0]
        puntero_stack_anterior = tupla_traductor[1]
        puntero_static_anterior= cant_static + tupla_traductor[2] + 1
        
        File_Output.writeFile(nombre_fichero_salida, code_assembly)
    
    
main()