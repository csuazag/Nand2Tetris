import File_In_Manipulation
import File_Out_Manipulation
import Analyzer_Lexical
import Translate

def main():    
    # Definir direccion del fichero de entrada
    adress_in = raw_input("Direccion del fichero de entrada")
    #Definir direccion del fichero de salida
    adress_out = raw_input("Direccion del fichero de salida")    

    code = File_In_Manipulation.controller_file_in(adress_in)     
    symbols_table = Analyzer_Lexical.controller_analyzer(code)
    binary = Translate.controller_traslate(code, symbols_table) 
    File_Out_Manipulation.controller_file_out(adress_out, binary)
    
main()
    
