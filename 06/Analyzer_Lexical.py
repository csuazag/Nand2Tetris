"""Este script realiza la primera pasada a todas las instrucciones
   en assembly.
   1. Se encarga de verificar que este bien escrito el codigo.
   2. Se encarga de llenar tabla de simbolos con instrucciones tipo a y labels.     
"""
syntax_numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
syntax_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
syntax_characters = ['_', '.', '$', ':']
dest = ['A', 'D', 'M', 'MD', 'AM', 'AD', 'AMD', '']
comp = ['0', '1', '-1', 'D', 'A', '!D', '!A', '-D', '-A', 'D+1', 'A+1', 'D-1', 'A-1', 'D+A', 'D-1', 'A-D', 'D&A', 'D|A', 'M', '!M', '-M', 'M+1', 'M-1', 'D+M', 'D-M', 'M-D', 'D&M', 'D|M']
jump = ['JGT', 'JEQ', 'JGE', 'JLT', 'JNE', 'JLE', 'JMP', '']
symbols_table = {'R0':0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5, 'R6':6, 'R7':7, 'R8':8, 'R9':9, 'R10':10, 'R11':11, 'R12':12, 'R13':13, 'R14':14, 'R15':15, 'SCREEN':16384, 'KBD':24576, 'SP':0, 'LCL':1, 'ARG':2, 'THIS':3, 'THAT':4}


""" Funcion encargada de verificar si el simbolo es correcto.
    Un simbolo no puede empezar por digito y puede contener una 
    serie de letras, digitos y algunos caracteres especiales."""
def check_symbol(value):
    if value[0] not in syntax_numbers:
        for i in value:
            if (i not in syntax_characters) and (i not in syntax_letters) and (i not in syntax_numbers):
                return False
        return True
    return False


""" Funcion encargada de verificar si toda la cadena son numeros """
def check_numbers(value):
    for i in value:
        if i not in syntax_numbers:
            return False
    return True
    
    
""" Funcion encargada de verificar sintaxis de un label """
def check_label(value):
    if value[-1] == ')' and check_symbol(value[1:-1].lower()):
        return True
    return False

        
""" Funcion encargada de verificar sintaxis de instruccion a """
def check_inst_a(value):
    value = value[1:]
    if check_numbers(value) or check_symbol(value.lower()):
        return True
    return False
    
        
""" Funcion encargada de verificar sintaxis de instruccion c.
    1. dest=comp;jump
    2. dest=comp
    3. comp;jump """
def check_inst_c(value):
    dest_str = ''
    comp_str = ''
    jump_str = ''

    if ('=' in value) and (';' in value):
        index1 = value.index('=')
        index2 = value.index(';')
        dest_str = value[:index1]
        comp_str = value[index1+1: index2]
        jump_str = value[index2+1:]       

    elif '=' in value:
        index = value.index('=')
        dest_str = value[:index]
        comp_str = value[index+1:]

    elif ';' in value:
        index = value.index(';')
        comp_str = value[:index]
        jump_str = value[index+1:]

    else: 
        return False
    
    if (dest_str in dest) and (comp_str in comp) and (jump_str in jump):
        return True
    return False
    
  
""" Funcion encargada de verificar la linea de codigo corresponde a:
    1. Instruccion a
    2. Etiqueta
    3. Instruccion c """
def correct_write(code_assembly):
    for i in code_assembly:        
        if len(i) > 1:
            answer = None
    
            if i[0] == '@':                
                answer = check_inst_a(i)
            elif i[0] == '(':
                answer = check_label(i)
            else:
                answer = check_inst_c(i)
            
            if not answer: return False
        else: 
            return False            
    return True
    

""" Metodo encargado de introducir a la tabla de simbolos los labels si no existen """
def append_symbols_table_labels(code):
    rom = 0   
    for i in code:
        if i[0] == '(':
            value = i[1:-1]
            if value not in symbols_table:                
                symbols_table[value] = rom            
            rom -= 1
        rom += 1


""" Metodo encargado de introducir a la tabla de simbolos las inst_a si no existen """
def append_symbols_table_inst_a(code):
    i_table = 16
    
    for i in code:
        if i[0] == '@':
            value = i[1:]            
            if check_numbers(value): 
                pass                
            elif value not in symbols_table:
                symbols_table[value] = i_table
                i_table += 1   
    

"""Controlador del script que recibe la lista del codigo en assembly dirige que funciones llamar"""
def controller_analyzer(code):
    if correct_write(code):
        append_symbols_table_labels(code)
        append_symbols_table_inst_a(code)
        print "Correct assembly syntax"
        print "Symbol table filled with success"
        return symbols_table
    else:
        print "Source code bad write"
        exit()
