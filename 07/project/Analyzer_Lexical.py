initial_index_stack = 256
final_index_stack = 2047

sp_stack = 256


out_vm = []
cont_labels = 0

"""Funcion para saber si la cantidad de elementos que hay en la pila cumple con la cantidad
    que se le envia por parametro. Sirve para analizar que cuando haga un add no se desborde 
    si solo he hecho un push o cuando se haga un pop no se desborde si no hay nada en la pila"""
def cant_stack(cantidad):
    res = sp_stack - initial_index_stack
    if res >= cantidad: return True, 'OK'
    return False, 'Invalid Operation because needed {0} into stack but only found {} elements'.format(cantidad, res)


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

    if   command == 'add':
        res = cant_stack(2)
        if res[0]: 
            line = '@SP{}M=M-1{}A=M{}D=M{}@SP{}M=M-1{}A=M{}M=M+D{}@SP{}M=M+1{}'.format('\n')
        else: 
            print res[1]
            exit()

    elif command == 'sub':
        res = cant_stack(2)
        if res[0] : 
            line = '@SP{}M=M-1{}A=M{}D=M{}@SP{}M=M-1{}A=M{}M=M-D{}@SP{}M=M+1{}'.format('\n')
        else:
            print res[1]
            exit() 

    elif command == 'eq':
        res = cant_stack(2)
        if res[0]:
            label_equal = 'EQUAL'.format(cont_labels)       #FORMAT -> 1
            label_end   = 'END_EQUAL'.format(cont_labels)   #FORMAT -> 2
        
            line = '@SP{}M=M-1{}A=M{}D=M{}@SP{}M=M-1{}A=M{}D=M-D{}@{1}{}D;JEQ{}@SP{}A=M{}M=0{}@{2}{}0;JMP{}({1}){}@SP{}A=M{}M=-1{}({2}){}@SP{}M=M+1{}'.format('\n', label_equal, label_end)
            cont_labels += 1
        else:
            print res[1]
            exit()

    elif command == 'gt':
        res = cant_stack(2)
        if res[0]:
            label_gt  = 'GREATHER_THAT'.format(cont_labels)      #FORMAT -> 1
            label_end = 'END_GREATHER_TAT'.format(cont_labels)   #FORMAT -> 2
            
            line = '@SP{}M=M-1{}A=M{}D=M{}@SP{}M=M-1{}A=M{}D=M-D{}@{1}{}D;JGT{}@SP{}A=M{}M=0{}@{2}{}0;JMP{}({1}){}@SP{}A=M{}M=-1{}({2}){}@SP{}M=M+1{}'.format('\n', label_gt, label_end)
            cont_labels += 1
        else:
            print res[1]
            exit()

    elif command == 'lt':
        res = cant_stack(2)
        if res[0]:
            label_lt  = 'LOWER_THAT'.fotmat(cont_labels)             #FORMAT -> 1
            label_end = 'END_LOWER_THAT'.format(cont_labels)         #FORMAT -> 2
            
            line = '@SP{}M=M-1{}A=M{}D=M{}@SP{}M=M-1{}A=M{}D=M-D{}@{1}{}D;JLT{}@SP{}A=M{}M=0{}@{2}{}0;JMP{}({1}){}@SP{}A=M{}M=-1{}({2}){}@SP{}M=M+1{}'.format('\n', label_gt, label_end)
            cont_labels += 1
        else:
            print res[1]
            exit()

    elif command == 'and':
        res = cant_stack(2)
        if res[0]:
            line = '@SP{}M=M-1{}A=M{}D=M{}@SP{}M=M-1{}A=M{}M=D&M{}@SP{}M=M+1{}'.format('\n')
        else:
            print res[1]
            exit()

    elif command == 'or' :
        res = cant_stack(2)
        if res[0]:
            line = '@SP{}M=M-1{}A=M{}D=M{}@SP{}M=M-1{}A=M{}M=D|M{}@SP{}M=M+1{}'.format('\n')
        else:
            print res[1]
            exit()

    elif command == 'not' :
        res = cant_stack(1)
        if res[0]:
            line = '@SP{}D=M-1{}A=D{}M=!M{}'.format('\n')
        else:
            print res[1]
            exit()

    elif command == 'neg':
        res = cant_stack(1)
        if res[0]:
            line = '@SP{}D=M-1{}A=D{}M=-M{}'.format('\n')
        else:
            print res[1]
            exit()

    else:
        print 'ERROR >> command not found'
        exit()        

    out_vm.append(line)


def writePush(li):
    
    response_overflow = check_not_overflow()

    if response_overflow[0] :
        
        memory_segment = li[1]
        number = int(li[2])
        line = ''

        if memory_segment == 'static':
            number += 16
            res = check_i_statics(number)
            if res[0]:
                line = '@{1}{}D=M{}@SP{}A=M{}M=D{}@SP{}M=M+1{}'.format('\n', number)                
            else: 
                print res[1]
                exit()

        elif memory_segment == 'temp':
            number += 5
            res = check_i_statics(number)

            if res[0]:
                line = '@{1}{}D=M{}@SP{}A=M{}M=D{}@SP{}M=M+1{}'.format('\n', number)                
            else: 
                print res[1]
                exit()
        
        elif memory_segment == 'constant':
            res = check_number_constant(number) 
            if res[0]:
                line = '@{1}{}D=A{}@SP{}A=M{}M=D{}@SP{}M=M+1{}'.format('\n', number)
            else:
                print res[1]
                
        elif memory_segment == 'argument':
            line = '@ARG{}D=M{}@{1}{}A=D+A{}D=M{}@SP{}A=M{}M=D{}@SP{}M=M+1{}'.format('\n', number)
                
        elif memory_segment == 'local':
            line = '@LCL{}D=M{}@{1}{}A=D+A{}D=M{}@SP{}A=M{}M=D{}@SP{}M=M+1{}'.format('\n', number)
                
        elif memory_segment == 'that':
            line = '@THAT{}D=M{}@{1}{}A=D+A{}D=M{}@SP{}A=M{}M=D{}@SP{}M=M+1{}'.format('\n', number)

        elif memory_segment == 'this':
            line = '@THIS{}D=M{}@{1}{}A=D+A{}D=M{}@SP{}A=M{}M=D{}@SP{}M=M+1{}'.format('\n', number)

        elif memory_segment == 'pointer' and number == 1:
            line = '@THAT{}A=M{}D=M{}@SP{}A=M{}M=D{}@SP{}M=M+1'.format('\n')

        elif memory_segment == 'pointer' and number == 0:
            line = '@THIS{}A=M{}D=M{}@SP{}A=M{}M=D{}@SP{}M=M+1'.format('\n')

        else:
            print 'Invalid Memory Segment'
            exit()

        sp_stack += 1
        out_vm.append(line)

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
            number += 16
            res = check_i_statics(number)
            if res[0]:
                line = '@SP{}M=M-1{}A=M{}D=M{}@{1}{}M=D{}'.format('\n', number)
            else:
                print res[1]
        
        elif memory_segment == 'temp':
            number += 5
            res = check_number_temp(number)            
            if res[0]:
                line = '@SP{}M=M-1{}A=M{}D=M{}@{1}{}M=D{}'.format('\n', number)
            else:
                print res[1]

        elif memory_segment == 'argument':
            line = '@SP{}M=M-1{}A=M{}D=M{}@ARG{}A=M{}M=D{}'.format('\n')

        elif memory_segment == 'local':
            line = '@SP{}M=M-1{}A=M{}D=M{}@LCL{}A=M{}M=D{}'.format('\n')

        elif memory_segment == 'that':
            line = '@SP{}M=M-1{}A=M{}D=M{}@THAT{}A=M{}M=D{}'.format('\n')

        elif memory_segment == 'this':
            line = '@SP{}M=M-1{}A=M{}D=M{}@THIS{}A=M{}M=D{}'.format('\n')

        elif (memory_segment == 'pointer') and (number == 1):
            line = '@SP{}M=M-1{}A=M{}D=M{}@THAT{}A=M{}M=D{}'.format('\n')
        
        elif (memory_segment == 'pointer') and (number == 0):
            line = '@SP{}M=M-1{}A=M{}D=M{}@THIS{}A=M{}M=D{}'.format('\n')
        
        else:
            print 'Invalid Memory Segment'
            exit()

        sp_stack -= 1
        out_vm.append(line)

    else:
        print res[1] + ', Function Write POP'
        exit()



def controller_translation(list_of_list):
    for li in list_of_list:
        if len(li) == 1:
            writeArithmetic(li)
        elif (li[0] == 'push') and (li[2].isdigit()):
            writePush(li)
        elif (li[0] == 'pop' ) and (li[2].isdigit()):
            writePop(li)
        else :
            print 'ERROR>>??'
            exit()
    print 'Successful Translation!!!!!!'
    

    

