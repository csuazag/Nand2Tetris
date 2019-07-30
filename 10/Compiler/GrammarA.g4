grammar GrammarA;

integerConstant : '0'
                | ('1'..'2')('0'..'9')?('0'..'9')?('0'..'9')?('0'..'9')?
                | ('3')('0'..'2')?('0'..'7')('0'..'6')('0'..'7')
                | ('4'..'9')('0'..'9')?('0'..'9')?('0'..'9')?;



StringConstant  : ('"') | ('A'..'Z')();

class           : 'class' className '{' classVarDec* subroutineDec* '}';

classVarDec     : ('static' | 'field') type varName (',' varName)* ';' ;

type            : 'int' 
                | 'char' 
                | 'boolean' 
                | className ; 

subroutineDec   : ('constructor' | 'function' | 'method') ('void' | type) subroutineName;

parameterList: ((type varName)(',' type varName)*)?;

subroutineBody: '{' varDec* statements '}';

varDec: 'var' type varName (',' varName)* ';';

className: identifier;

subroutineName: identifier;

varName: identifier;

statements: statement*;

statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement ;

letStatement: 'let' varName ('[' expression ']')? '=' expression ';' ;

ifStatement: 'if' '(' expression ')' '(' '{' statements '}' ('else' '{' statements '}')?;

whileStatement: 'while' '(' expression ')' '{' statements '}';

doStatement: 'do' subroutineCall ';';

ReturnStatement: 'return' expression? ';';

expression: term (op term)*;

term: integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' unaryOp term ;

subroutineCall: subroutineName '(' expressionList ')' | (className | varName) '.' subroutineName '(' expressionList ')';

expressionList: (expression (',' expression)*)?;

op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=';

unaryOp: '-' | '~';

keywordConstant: 'true' | 'false' | 'null' | 'this';







