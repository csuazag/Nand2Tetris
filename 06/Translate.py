""" Script encargado de recibir el codigo en assembly y traducirlo a binario, luego se crea file.asm con el binario."""
from Analyzer_Lexical import check_numbers

code = None
symbols_table = None
binary_code = []

map_destination = {'null':'000', 'M':'001', 'D':'010', 'MD':'011', 'A':'100', 'AM':'101', 'AD':'110', 'AMD':'111'}
map_jump = {'null':'000', 'JGT':'001', 'JEQ':'010', 'JGE':'011', 'JLT':'100', 'JNE':'101', 'JLE':'110', 'JMP':'111'}
map_comp0 = {'0':'101010', '1':'111111', '-1':'111010', 'D':'001100', 'A':'110000', '!D':'001101', '!A':'110001', '-D':'001111', '-A':'110011', 'D+1':'011111', 'A+1':'110111', 'D-1':'001110', 'A-1':'110010', 'D+A':'000010', 'D-A':'010011', 'A-D':'000111', 'D&A':'000000', 'D|A':'010101'}
map_comp1 = {'M':map_comp0['A'],  '!M':map_comp0['!A'], '-M':map_comp0['-A'], 'M+1':map_comp0['A+1'], 'M-1':map_comp0['A-1'], 'D+M':map_comp0['D+A'], 'D-M':map_comp0['D-A'], 'M-D':map_comp0['A-D'], 'D&M':map_comp0['D&A'], 'D|M':map_comp0['D|A']}


""" Metodo encargada de encontrar el valor binario en los maps, luego se agrega a la lista binary_code"""
def build_c(dest, comp, jump):
    line = "111"
    if comp in map_comp0:
        line += '0' + map_comp0[comp]
    else:
        line += '1' + map_comp1[comp]    
    line += map_destination[dest]
    line += map_jump[jump]

    binary_code.append(line)


""" Metodo encargado de hallar valores dest, comp, jump. Posterior invoca el metodo check_c """
def select_c(value):
    dest = 'null'
    comp = 'null'
    jump = 'null'

    if ('=' in value) and (';' in value):
        index1 = value.index('=')
        index2 = value.index(';')

        dest = value[:index1]
        comp = value[index1+1: index2]
        jump = value[index2+1:]       

    elif '=' in value:
        index = value.index('=')

        dest = value[:index]
        comp = value[index+1:]

    elif ';' in value:
        index = value.index(';')

        comp = value[:index]
        jump = value[index+1:]

    build_c(dest, comp, jump)


""" Metodo encargado de tomar la instruccion a, si se encuentra con variable saber su direccion buscando
    en la tabla de simbolos y luego traduciendo a binario, posterior se agrega a lista binary_code """
def build_a(value):
    value = value[1:]
    line = "0"
    add = ""
    if check_numbers(value):
        add += bin(int(value))[2:] 
    else:
        number = int(symbols_table[value])
        add += bin(number)[2:] 
    
    sub = 15 - len(add)
    if sub >= 0:
        line += '0'*sub + add
    else:
        print("OVERFLOW")
        exit()
    binary_code.append(line)


""" Metodo encargado de dirigir la traduccion de Assembler a binario"""
def controller_traslate(code_in, symbols_table_in):
    global code, symbols_table
    code = code_in
    symbols_table = symbols_table_in

    for i in code:        
        if i[0] == '@':                
            build_a(i)
        elif i[0] == '(':
            pass            
        else:
            select_c(i)
    print 'Correct translation'
    return binary_code

       
