~~~ kleines de bach ~~~

Main |:
	<!> "Hallo Bach! Escriu dos valors:"
	<?> a
	<?> b
	if a>b |:
		a <- 5
	:|

	~~~ provant funcions llistes ~~~
	<!> "valor d'a: " a

	~~~ a sota declarem una llista ~~~
	l <- {1 2 3 4 5}
	<!> l[0]
	<!> #l
	8< l[0] 
	<!> l

	~~~ús condicionals~~~
	if a>b |:
		a <- a+b
	:|
	else |:
		a <- 50
	:|

	~~~ prova de cridar a un procediment i posteriorment s'executa ~~~
	Suma a b
	<!> a

	~~~ vinga va i ara una mica de notes! ~~~
	<:> {D E F G A A}
	<:> {C D E F G2 G2 G2 C2 D C B A B2 C B A G F2 G A B G A2 D C B A A2 B A G F G3}
:|

~~~ declaració del procediment ~~~
Suma a b |:
	<!> a
	a <- a+b
	<!> a
:|