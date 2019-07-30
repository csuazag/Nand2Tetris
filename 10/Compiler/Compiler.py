
import sys
from os import listdir

from antlr4 import *
from JackLexer import JackLexer
from JackParser import JackParser
from antlr4.tree.Trees import Trees
from antlr4.error.ErrorListener import ErrorListener


class MyErrorListener( ErrorListener ):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        stack = recognizer.getRuleInvocationStack()
        stack.reverse()
        print (str(line) + ":" + str(column) + ": sintax ERROR, " + str(msg))
        print ("Terminating Translation")
        sys.exit()


def main(argv):
    

    ruta_carpeta = argv[1]
    print (ruta_carpeta)

    files = []
    for i in listdir(ruta_carpeta):
        if i.find('.jack') != -1: files.append(i)

    for i in files:
        input  = FileStream(ruta_carpeta + "/" + i)
        lexer  = JackLexer(input)
        stream = CommonTokenStream(lexer)
        parser = JackParser(stream)
        parser.addErrorListener(MyErrorListener())
        tree   = parser.classJack()

        print (ruta_carpeta + "/" + i[:-4] + "xml")
        archivo1 = open(ruta_carpeta + "/" + i[:-5] + "xml", "w")
        archivo1.write(parser.xml_analyzer)
        archivo1.close()

        archivo2 = open(ruta_carpeta + "/" + i[:-5] + "Txml", "w")
        archivo2.write(parser.xml_tokens)
        archivo2.close()

    



    
 
if __name__ == '__main__':
    main(sys.argv)