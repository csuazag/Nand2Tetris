grammar Jack;
options{
language=Python3;
}
classJack:
	'class' className '{' (classVarDec)* (subroutineDec)* '}';

classVarDec: ('static' | 'field') jacktype varName (',' varName)* ';';

jacktype: 'int' | 'char' | 'boolean' | className;

subroutineDec: ('constructor' | 'function' | 'method') ('void' 	| jacktype ) subroutineName '(' parameterList ')' subroutineBody;

parameterList: ((jacktype varName) (',' jacktype varName)*)?;

subroutineBody: '{' (varDec)* statements '}';

varDec: 'var' jacktype varName (',' varName)* ';';

className: IDENTIFIER;

subroutineName: IDENTIFIER;

varName: IDENTIFIER;

statements: statement*;

statement:
	letStatement
	| ifStatement
	| whileStatement
	| doStatement
	| returnStatement;

letStatement:
	'let' varName ('[' expression ']')? '=' expression ';';

ifStatement:
	'if' '(' expression ')' '{' statements '}' (
		'else' '{' statements '}'
	)?;

whileStatement: 'while' '(' expression ')' '{' statements '}';

doStatement: 'do' subroutineCall ';';

returnStatement: 'return' expression? ';';

expression: term (op term)*;

term:
	INTEGERCONSTANT
	| STRINGCONSTANT
	| keywordConstant
	| varName
	| varName '[' expression ']'
	| subroutineCall
	| '(' expression ')'
	| unaryOp term;

subroutineCall:
	subroutineName '(' expressionList ')'
	| (className | varName) '.' subroutineName '(' expressionList ')';

expressionList: (expression (',' expression)*)?;

op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=';

unaryOp: '-' | '~';

keywordConstant: 'true' | 'false' | 'null' | 'this';


INTEGERCONSTANT: ('0' .. '9')
	| ('1' .. '9') ('0' .. '9')
	| ('1' .. '9') ('0' .. '9') ('0' .. '9')
	| ('1' .. '9') ('0' .. '9') ('0' .. '9') ('0' .. '9')
	| ('1' .. '3') ('0' .. '2') ('0' .. '7') ('0' .. '6') (
		'0' .. '7'
	);

STRINGCONSTANT: '"' ~('\r' | '\n' | '"')* '"';

IDENTIFIER: (('A' ..'Z') | ('a' ..'z') | '_')+ (
		('A' ..'Z')
		| ('a' ..'z')
		| '_'
		| ('0' ..'9')
	)*;
BLOCKCOMMENT: '/*' .*? '*/' -> skip;
COMMENT: '//' ~('\n'|'\r')* -> skip; 
WHITESPACE: (' '|'\t')+ ->     skip; 
JUMPLINE: ('\n'|'\r')+ ->      skip; 