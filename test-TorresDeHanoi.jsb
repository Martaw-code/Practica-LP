Main |:
    <!> "Escriu un nombre: "
    <?> n
    Hanoi n 1 2 3
:|

Hanoi n ori dst aux |:
    if n>0 |:
        Hanoi (n-1) ori aux dst
        <!> ori "->" dst
        Hanoi (n-1) aux dst ori
    :|
:|