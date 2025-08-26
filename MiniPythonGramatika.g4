grammar MiniPythonGramatika;

//--------------------------------
// pravila lexera
//--------------------------------

DEF: 'def' ;
IF: 'if' ;
ELSE: 'else' ;
WHILE: 'while' ;
FOR: 'for' ;
IN: 'in' ;
RETURN: 'return' ;
PRINT: 'print' ;
RANGE: 'range' ;
LEN: 'len' ;

LPAREN: '(' ;
RPAREN: ')' ;
LBRACE: '{' ;
RBRACE: '}' ;
LBRACK: '[' ;
RBRACK: ']' ;
LBRACESET: '<|' ;
RBRACESET: '|>' ;
COLON: ':' ;
COMMA: ',' ;
SEMI: ';' ;
ASSIGN: '=' ;
PLUS: '+' ;
MINUS: '-' ;
MUL: '*' ;
DIV: '/' ;
MOD: '%' ;
EQ: '==' ;
NEQ: '!=' ;
LT: '<' ;
GT: '>' ;
LE: '<=' ;
GE: '>=' ;

ID: [a-zA-Z_][a-zA-Z_0-9]* ;
FLOAT: [0-9]+ '.' [0-9]+ ;
INT: [0-9]+ ;
STRING: '"' (~["\\] | '\\' .)* '"' ;

WS: [ \t\r\n]+ -> skip ; 
COMMENT: '#' ~[\r\n]* -> skip ;

//--------------------------------
// pravila parsera
//--------------------------------

program: statement* EOF ;

statement
	: simple_stmt
	| compound_stmt
	;
	
simple_stmt
	: assignment
	| print_stmt
	| return_stmt
	| function_call
	;
	
assignment: ID ASSIGN expr ;

print_stmt: PRINT LPAREN (expr (COMMA expr)*)? RPAREN ;

return_stmt: RETURN expr? ;

function_call
	: ID LPAREN (expr (COMMA expr)*)? RPAREN
	;

compound_stmt
	: if_stmt
	| while_loop
	| for_loop
	| function_def
	;
	
if_stmt
	: IF LPAREN expr RPAREN block (ELSE block)?
	;
	
while_loop
	: WHILE LPAREN expr RPAREN block
	;
	
for_loop
	: FOR ID IN range_expr block
	;
	
range_expr
	: RANGE LPAREN expr (COMMA expr (COMMA expr)?)? RPAREN
	;
	
function_def
	: DEF ID LPAREN param_list? RPAREN block
	;
	
param_list
	: ID (COMMA ID)*
	;
	
block
	: LBRACESET statement* RBRACESET
	;

list_expr
	: LBRACK (expr (COMMA expr)*)? RBRACK
	;
	
tuple_expr
	: LPAREN expr (COMMA expr)+ RPAREN
	;

set_expr
	: LBRACE ( expr (COMMA expr)*)? RBRACE
	;

expr
	: expr op=(MUL | DIV | MOD) expr
	| expr op=(PLUS | MINUS) expr
	| expr op=(EQ|NEQ|LT|LE|GT|GE) expr
	| LPAREN expr RPAREN
	| ID
	| INT
	| FLOAT
	| STRING
	| '(' expr ')'
	| function_call
	| list_expr
	| tuple_expr
	| set_expr
	;


