initial_index_stack = 256
final_index_stack = 2047

sp_stack = 0            #Posicion actual del SP
pointer_static = 0      #Variable que me dice cual es el puntero del static para cuidar de la memoria en la traduccion. de cada los .vm, es decir, evitar sobreescritura de un static por otro.vm
file_name = ''            #Nombre del fichero actual a traducir

out_assembly = []       #Lista de escritura del codigo en assembly

cont_labels = 0         #Contador para cuando se crean (LABELS) en assembly y diferenciarlos por el numero


"""Funcion para saber si la cantidad de elementos que hay en la pila cumple con la cantidad
    que se le envia por parametro. Sirve para analizar que cuando haga un add no se desborde 
    si solo he hecho un push o cuando se haga un pop no se desborde si no hay nada en la pila"""
def cant_stack(cantidad):
    res = sp_stack - initial_index_stack
    if res >= cantidad: return True, 'OK'
    return False, 'Invalid Operation because needed {0} into stack but only found {1} elements'.format(cantidad, res)


"""Verificar que el numero cuando es static no se desborde ni superior ni inferior en su segmento mapeado """
def check_i_statics(index):
    if (index >= 16) and (index <= 255):
        return True, 'Ok'
    elif (index < 16):
        return False, 'ERROR >> Bottom Overflow of the Static Segment!! -> static_segment < 16 Incorrect'    
    return False, 'ERROR >> Top Overflow of the Static Segment !! -> static_segment > 255 Incorrect'
    

"""Verificar que el numero no sea mayor de 16 bits ni sea un numero negativo"""
def check_number_constant(number):
    if (number >= 0) and (number <= 65535):
        return True, 'Ok'
    elif (number < 0):
        return False, 'ERROR >> Negative numbers are not allowed'
    return False, 'ERROR >> Only 16-bit numbers are allowed'


"""Verificar que el numero se encuentre en el rango del temp"""
def check_number_temp(number):
    if (number >= 5) and (number <= 12):
        return True, 'Ok'
    elif (number < 5):
        return False, 'ERROR >> Only numbers greather that 5'    
    return False, 'ERROR >> Only numbers lower that 12'
    

"""Verificar que SP no se haya desbordado inferior ni superior"""
def check_not_overflow():
    if (sp_stack >= initial_index_stack) and (sp_stack <= final_index_stack):
        return True, 'OK'
    elif (sp_stack < initial_index_stack):
        return False, 'ERROR >> Bottom overflow of the stack pointer, SP < {} Incorrect'.format(initial_index_stack)
    return False, 'ERROR >> Top overflow of the stack pointer, SP > {} Incorrect'.format(final_index_stack)
    

def writeArithmetic(li):
    command = li[0]
    line = ''
    global cont_labels

    if   command == 'add':
        res = cant_stack(2)
        if res[0]: 
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@SP{0}M=M-1{0}A=M{0}M=M+D{0}@SP{0}M=M+1{0}'.format('\n')
        else: 
            print res[1]
            exit()

    elif command == 'sub':
        res = cant_stack(2)
        if res[0] : 
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@SP{0}M=M-1{0}A=M{0}M=M-D{0}@SP{0}M=M+1{0}'.format('\n')
        else:
            print res[1]
            exit() 

    elif command == 'eq':
        res = cant_stack(2)
        if res[0]:            
            label_equal = 'EQUAL{}'.format(cont_labels)       #FORMAT -> 1
            label_end   = 'END_EQUAL{}'.format(cont_labels)   #FORMAT -> 2
        
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@SP{0}M=M-1{0}A=M{0}D=M-D{0}@{1}{0}D;JEQ{0}@SP{0}A=M{0}M=0{0}@{2}{0}0;JMP{0}({1}){0}@SP{0}A=M{0}M=-1{0}({2}){0}@SP{0}M=M+1{0}'.format('\n', label_equal, label_end)
            cont_labels += 1
        else:
            print res[1]
            exit()

    elif command == 'gt':
        res = cant_stack(2)
        if res[0]:
            label_gt  = 'GREATHER_THAT{}'.format(cont_labels)      #FORMAT -> 1
            label_end = 'END_GREATHER_TAT{}'.format(cont_labels)   #FORMAT -> 2
            
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@SP{0}M=M-1{0}A=M{0}D=M-D{0}@{1}{0}D;JGT{0}@SP{0}A=M{0}M=0{0}@{2}{0}0;JMP{0}({1}){0}@SP{0}A=M{0}M=-1{0}({2}){0}@SP{0}M=M+1{0}'.format('\n', label_gt, label_end)
            cont_labels += 1
        else:
            print res[1]
            exit()

    elif command == 'lt':
        res = cant_stack(2)
        if res[0]:
            label_lt  = 'LOWER_THAT{}'.format(cont_labels)             #FORMAT -> 1
            label_end = 'END_LOWER_THAT{}'.format(cont_labels)         #FORMAT -> 2
            
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@SP{0}M=M-1{0}A=M{0}D=M-D{0}@{1}{0}D;JLT{0}@SP{0}A=M{0}M=0{0}@{2}{0}0;JMP{0}({1}){0}@SP{0}A=M{0}M=-1{0}({2}){0}@SP{0}M=M+1{0}'.format('\n', label_lt, label_end)
            cont_labels += 1
        else:
            print res[1]
            exit()

    elif command == 'and':
        res = cant_stack(2)
        if res[0]:
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@SP{0}M=M-1{0}A=M{0}M=D&M{0}@SP{0}M=M+1{0}'.format('\n')
        else:
            print res[1]
            exit()

    elif command == 'or' :
        res = cant_stack(2)
        if res[0]:
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@SP{0}M=M-1{0}A=M{0}M=D|M{0}@SP{0}M=M+1{0}'.format('\n')
        else:
            print res[1]
            exit()

    elif command == 'not' :
        res = cant_stack(1)
        if res[0]:
            line = '@SP{0}D=M-1{0}A=D{0}M=!M{0}'.format('\n')
        else:
            print res[1]
            exit()

    elif command == 'neg':
        res = cant_stack(1)
        if res[0]:
            line = '@SP{0}D=M-1{0}A=D{0}M=-M{0}'.format('\n')
        else:
            print res[1]
            exit()

    else:
        print 'ERROR >> command not found'
        exit()        

    out_assembly.append(line)


def writePush(li):
    
    response_overflow = check_not_overflow()

    if response_overflow[0] :
        
        memory_segment = li[1]
        number = int(li[2])
        line = ''

        if memory_segment == 'static':
            number += pointer_static
            res = check_i_statics(number)
            if res[0]:
                line = '@{1}{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', number)                
            else: 
                print res[1]
                exit()

        elif memory_segment == 'temp':
            number += 5
            res = check_number_temp(number)

            if res[0]:
                line = '@{1}{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', number)                
            else: 
                print res[1]
                exit()
        
        elif memory_segment == 'constant':
            res = check_number_constant(number) 
            if res[0]:
                line = '@{1}{0}D=A{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', number)
            else:
                print res[1]
                exit()
                
        elif memory_segment == 'argument':
            line = '@ARG{0}D=M{0}@{1}{0}A=D+A{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', number)
                
        elif memory_segment == 'local':
            line = '@LCL{0}D=M{0}@{1}{0}A=D+A{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', number)
                
        elif memory_segment == 'that':
            line = '@THAT{0}D=M{0}@{1}{0}A=D+A{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', number)

        elif memory_segment == 'this':
            line = '@THIS{0}D=M{0}@{1}{0}A=D+A{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', number)

        elif memory_segment == 'pointer' and number == 1:
            line = '@THAT{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n')

        elif memory_segment == 'pointer' and number == 0:
            line = '@THIS{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n')

        else:
            print 'Invalid Memory Segment'
            exit()

        global sp_stack
        sp_stack += 1
        out_assembly.append(line)

    else:
        print res[1] + ', Function Write PUSH'
        exit()


def writePop(li):
    
    response_overflow = check_not_overflow()
    
    if response_overflow[0] :
        
        memory_segment = li[1]
        number = int(li[2])
        line = ''

        if memory_segment == 'static':
            number += pointer_static
            res = check_i_statics(number)
            if res[0]:
                line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@{1}{0}M=D{0}'.format('\n', number)
            else:
                print res[1]
                exit()
        
        elif memory_segment == 'temp':
            number += 5
            res = check_number_temp(number)            
            if res[0]:
                line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@{1}{0}M=D{0}'.format('\n', number)
            else:
                print res[1]
                exit()

        elif memory_segment == 'argument':
            line = '@{1}{0}D=A{0}@ARG{0}D=M+D{0}@R15{0}M=D{0}@SP{0}AM=M-1{0}D=M{0}@R15{0}A=M{0}M=D{0}'.format('\n', number)

        elif memory_segment == 'local':
            line = '@{1}{0}D=A{0}@LCL{0}D=M+D{0}@R15{0}M=D{0}@SP{0}AM=M-1{0}D=M{0}@R15{0}A=M{0}M=D{0}'.format('\n', number)

        elif memory_segment == 'that':
            line = '@{1}{0}D=A{0}@THAT{0}D=M+D{0}@R15{0}M=D{0}@SP{0}AM=M-1{0}D=M{0}@R15{0}A=M{0}M=D{0}'.format('\n', number)

        elif memory_segment == 'this':
            line = '@{1}{0}D=A{0}@THIS{0}D=M+D{0}@R15{0}M=D{0}@SP{0}AM=M-1{0}D=M{0}@R15{0}A=M{0}M=D{0}'.format('\n', number)

        elif (memory_segment == 'pointer') and (number == 1):
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@THAT{0}M=D{0}'.format('\n')
        
        elif (memory_segment == 'pointer') and (number == 0):
            line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@THIS{0}M=D{0}'.format('\n')
        
        else:
            print 'Invalid Memory Segment'
            exit()

        global sp_stack
        sp_stack -= 1
        out_assembly.append(line)

    else:
        print res[1] + ', Function Write POP'
        exit()


def writeLabel(li):
    c = li[1]
    line = '({1}){0}'.format('\n', c)
    out_assembly.append(line)


def writeGoto(li):
    c = li[1]
    line = '@{1}{0}0;JMP{0}'.format('\n', c)
    out_assembly.append(line)


def writeIfGoto(li):
    c = li[1]
    line = '@SP{0}M=M-1{0}A=M{0}D=M{0}@{1}{0}D;JNE{0}'.format('\n', c)
    out_assembly.append(line)


def writeCall(li):
    function_name = li[1]
    num_args = int(li[2])

    global cont_labels, sp_stack

    label = 'RETURN_LABEL{0}'.format(cont_labels)
    #Guardar en pila la direccion de retorno
    line = '@{1}{0}D=A{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', label)

    #Guardar en pila la direccion de los segmentos LCL,ARG,THIS,THAT
    line += '@{1}{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', 'LCL')
    line += '@{1}{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', 'ARG')
    line += '@{1}{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', 'THIS')
    line += '@{1}{0}D=M{0}@SP{0}A=M{0}M=D{0}@SP{0}M=M+1{0}'.format('\n', 'THAT')
            
    #Guardar la nueva direccion de ARG
    line += '@SP{0}D=M{0}@{1}{0}D=D-A{0}@5{0}D=D-A{0}@ARG{0}M=D{0}'.format('\n',num_args)
    #Guardar la nueva direccion de LCL
    line += '@SP{0}D=M{0}@LCL{0}M=D{0}'.format('\n')
    #Goto funcion g
    line += '@{1}{0}0;JMP{0}'.format('\n', function_name)
    line += '({1}){0}'.format('\n', label)

    out_assembly.append(line)
    cont_labels += 1
    sp_stack += 5


def writeFunction(li):
    function_name = li[1]
    num_vars = int(li[2])

    line = '({1}){0}'.format('\n', function_name)
    out_assembly.append(line)

    for i in range(num_vars):
        writePush(['push','constant','0'])


def writeReturn(li):   
    
    #frame = LCL
    line = '@LCL{0}D=M{0}@R14{0}M=D{0}'.format('\n')
    #retAddr = *(frame-5)
    line += '@R14{0}D=M{0}@5{0}D=D-A{0}A=D{0}D=M{0}@R13{0}M=D{0}'.format('\n')
    #*ARG = pop
    line += '@SP{0}M=M-1{0}A=M{0}D=M{0}@ARG{0}A=M{0}M=D{0}'.format('\n')
    #SP=ARG+1
    line += '@ARG{0}D=M+1{0}@SP{0}M=D{0}'.format('\n')
    #THAT = *(frame-1)
    line += '@R14{0}D=M{0}@1{0}D=D-A{0}A=D{0}D=M{0}@THAT{0}M=D{0}'.format('\n')
    #THIS = *(frame-2)
    line += '@R14{0}D=M{0}@2{0}D=D-A{0}A=D{0}D=M{0}@THIS{0}M=D{0}'.format('\n')
    #ARG = *(frame-3)
    line += '@R14{0}D=M{0}@3{0}D=D-A{0}A=D{0}D=M{0}@ARG{0}M=D{0}'.format('\n')
    #LCL = *(frame-4)
    line += '@R14{0}D=M{0}@4{0}D=D-A{0}A=D{0}D=M{0}@LCL{0}M=D{0}'.format('\n')
    #goto retAddr
    line += '@R13{0}A=M{0}0;JMP{0}'.format('\n')

    out_assembly.append(line)

    global sp_stack
    sp_stack -= 1


def writeInit():
    line = '@256{0}D=A{0}@SP{0}M=D{0}'.format('\n')
    out_assembly.append(line)
    writeCall(['call', 'Sys.init', '0'])    
    
    

""" Funcion controladora que selecciona la linea de VM y define si se hace un push, pop o una
    operacion aritmetica"""
def controller_translation(existe_sysvm, name_vm, list_of_list, sp_actual = 256, arranca_static = 16):
    global sp_stack, pointer_static, file_name
    sp_stack = sp_actual
    pointer_static = arranca_static
    file_name = name_vm

    if existe_sysvm: writeInit()
    
    for li in list_of_list:
        
        if len(li) == 1:
            if li[0] == 'return': writeReturn(li)
            else: writeArithmetic(li)

        elif len(li) == 2:
            if   li[0] == 'label'  : writeLabel(li)
            elif li[0] == 'goto'   : writeGoto(li)
            elif li[0] == 'if-goto': writeIfGoto(li)
            else:
                print 'ERROR>>??'.format(li)
                exit()

        elif len(li) == 3:
            if   li[0] == 'push' and li[2].isdigit() : writePush(li)
            elif li[0] == 'pop'  and li[2].isdigit() : writePop(li)
            elif li[0] == 'call'    : writeCall(li)
            elif li[0] == 'function': writeFunction(li)             
            else :
                print 'ERROR>>??'.format(li)
                exit()
        else:
            print 'ERROR>>??JAJA'.format(li)
            exit()


    return out_assembly, sp_stack, pointer_static
    

    

