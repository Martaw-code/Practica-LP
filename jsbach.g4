grammar jsbach;

root : (declaraFuncio)* main (declaraFuncio)* EOF;

main: 'Main' ' ' '|:' instruction+ ':|' ;

instruction: assignacio 
    | lectura 
    | reproduccio
    | escriptura
    | condicional
    | loopWhile 
    | cridaProc
    | afegeix
    | elimina
    ;

expr : '(' expr ')'                             
    | expr (MUL | DIV | MOD) expr                  
    | expr (MES | RESTA) expr                  
    | NUM
    | llargada
    | consulta                                          
    | VAR 
    | NOTA                                                                                
    ;

operadorRelacional : EQ | GT | LT | NEQ | GTE | LTE;

NOTA   : [A-G] [0-8]?;
NUM    : [0-9]+ ;
VAR    : [a-z] [a-zA-Z]*;
FUNC   : [A-Z] [a-zA-Z]*;

//---OPERADORS ARITMÈTICS---//

MES   : '+';    
RESTA : '-';
MUL   : '*';
DIV   : '/';
MOD   : '%';

//---OPERADORS RELACIONALS---//

EQ  : '=';
GT  : '>';
LT  : '<';
NEQ : '/='; 
GTE : '>=';
LTE : '<=';


//-----ESPECIFICACIÓ LLENGUATGE-----//

assignacio   : VAR ' <- ' (expr | llista);
lectura      : '<?> ' VAR; 
escriptura   : '<!>' (' ' blocText|' 'expr)*;
reproduccio  : '<:> ' (expr | llista) ;

TEXT     : '"' ~["]* '"' ;
blocText : (TEXT);

condicional       : (condicionalIf | condicionalIfElse);
condicionalIfElse : 'if' ' ' (expr) operadorRelacional (expr) ' ' '|:' (instruction)+ ':|' 'else' ' ' '|:' (instruction)+ ':|';
condicionalIf     : 'if' ' ' (expr) operadorRelacional (expr) ' ' '|:' (instruction)+ ':|';

loopWhile         : 'while' ' ' (expr) operadorRelacional (expr) ' ' '|:' (instruction)+ ':|';

cjtVar  : (VAR(' ' VAR)*)?;

declaraFuncio       : FUNC ' ' (VAR (' ' VAR)* ' ')? '|:' (instruction)+ ':|';
cridaProc           : FUNC ' ' (expr (' ' expr)*)?;

llista   : '{' (expr(' ' expr)*)? '}';
llargada : '#' VAR;
consulta : VAR '[' expr ']';
afegeix  : VAR ' ' '<<' ' ' expr;
elimina  : '8<' ' ' VAR '[' expr ']';

WS : [ \t\r\n]+ -> skip ;

COMENTARI : '~~~' .*? '~~~' -> skip;
