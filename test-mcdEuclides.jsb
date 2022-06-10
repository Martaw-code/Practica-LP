~~~ programa que llegeix dos enters i n'escriu el seu maxim comu divisor ~~~

Main |:
    <!> "Escriu dos nombres: "
    <?> a
    <?> b
    Euclides a b
:|

Euclides a b |:
    while a/=b |:
        if a>b |:
            a <- a-b
        :| 
        else |:
            b <- b-a
        :|
    :|
    <!> "El seu MCD es: " a
:|