import sys
import File_Input
import Translator
import File_Output

def main():    
    # Definir direccion del fichero de entrada
    adress_in = sys.argv[1]
    
    #Definir direccion del fichero de salida
    adress_out = adress_in[:-3] + ('.asm')

    code_vm = File_Input.controller_file_in(adress_in)     
    
    code_assembly = Translator.controller_translation(code_vm)

    File_Output.writeFile(adress_out, code_assembly)

    
    
main()