# El doble intèrpret de JSBach 🎼🎶
Aquest projecte té la comesa d'implementar un ***doble intèrpret*** per al llenguatge de programació musical anomenat JSBach. 

Aquest *doble intèrpret* no és res més que l'intèrpret del llenguatge de programació JSBach. Tot i això, ja que l'ideòleg de la gramàtica d'aquest llenguatge musical és el gran compositor Bach, el volem ajudar alhora de visualitzar i interpretar les seves creacions.

Per fer-ho, la idea d'aquest *doble intèrpret* serà de poder proporcionar al propi creador del llenguatge musical o a qualsevol músic, una partitura i uns fitxers de so amb la interpretació de qualsevol peça composada amb el llenguatge JSBach 

Per tant, amb l'escriptura de qualsevol peça amb JSBach, l'interpret te'n generarà una partitura i uns àudios amb la melodia.

## Qui hi trobaràs en aquest projecte?
Aquest projecte es divideix en 4 parts:
* jsbach.g4: implementa la gramàtica del *doble intèrpret*
* jsbach.py: implementa el programa de l'interpret del llenguatge el qual ens permetrà executar els programes escrits en JSBach. (**A dins trobarem els *visitors* que conté el programa.**)
* `test-*.jsb`: conjunt de fitxers escrits en JSBach que ens són útils per provar el funcionament de *doble intèrpret*
* `Makefile`: ens permet agilitzar el procés d'obtenció de fitxers i ens permet executar l'intèrpret.
## Comencem!
Les següents instruccions us ajudaran a instal·lar-vos tots els requisits previs per executar i utilitzar JSBach, com així els programes externs per generar les partitures i els fitxers de so que produirà el vostre *doble intèrpret*.
### Prerequisits
Anem per feina! Abans però és imprescindible instal·lar els requeriments per a Python i també els paquets necessaris per poder executar el nostre intèrpret.
### Instal·lació
Per instal·lar els requeriments per a Python i instal·lar `ANTLR4`, executarem:

    pip3 install antlr4-python3-runtime
Cal notar que s'ha desenvolupat aquesta versió de l'intèrpret amb la versió de Python: 3.9.13

També, per poder fer ús dels programes externs per generar les partitures i els fitxers de so, és necessari instal·lar-se les diverses eines que ho fan possibles mitjançant diversos paquets. Ho podeu fer amb el vostre gestor preferit. 
En el meu cas jo treball amb OSX i ho ho het mitjançant: **Homebrew**, executant les comandes des de la terminal:

    brew instal lilypond

**Lilypond** us permetrà generar les partitures ja que s'encarregarà de generar els fitxers: `MIDI` i `PDF`

    brew install timidity
**Timidity++** s'encarregarà de generar el fitxer `WAV` a partir de `MIDI` generat anteriorment

    brew install ffmpeg
**FFmpeg** d'altra banda us generarà el fitxer de `MP3` a partir de `WAV` anterior.

Podeu executar un fitxer `MP3`de moltes formes diferents. Si teniu el reproductor **VLC** ja us bastarà per poder sentir la melodia.

---
Un cop hagueu seguit el procediment d'instal·lació anterior, ja esteu un pas més a prop de poder executar el vostre *doble intèrpret*, només us caldrà abans de seguir, generar els fitxers necessaris(Lexer, Parser i tokens) a partir de la gramàtica amb la comanda:

    make gramatica

### Com executar l'intèrpret
Un cop arribats aquí, ja tot és planer i només haureu de decidir com inicieu el vostre programa. O bé podeu fer-ho executant:

    python3 jsbach.py nomPrograma.jsb

O bé, passant com a paràmetre el nom del procediment que voleu començar executant, i si s'escau, també li haureu de passar els paràmetres que necessiti:

    python3 jsbach.py nomPrograma.jsb nomProcediment p1 p2 p3 ... pn

Altrament, podeu considerar fer servir el `Makefile`que es troba disponible al projecte i executant la comanda: `make` us permetrà executar el fitxer `test-HalloBach.jsb` com un primer exemple de com funciona l'intèrpret.

Si ho desitgeu, posteriorment podeu canviar la comanda del Makefile i canviar el nom de l'arxiu `test-HalloBach.jsb`  de la comanda `make` pel que preferiu.

A més, si voleu provar la funcionalitat de cada joc de proves, podeu executar la comanda:

    make joc*

On l'asterisc el podeu substituir per un nombre de l'1 al 5 amb els possibles jocs de proves que es troben disponibles.

Si necessiteu desfer-vos de tots els fitxers generats per la gramàtica, com per les partitures i els fitxers de so, i voleu netejar una mica la carpeta on estigueu executant el programa, podeu fer-ho amb:

    make clean

## Informació sobre el doble intèrpret
La gramàtica del nostre intèrpret s'ha construït segons les directius donades per Bach i es troben actualment recollides a l'enunciat de la pràctica(veure Referències).
Nogensmenys, és precís donar una sèrie de clarificacions i d'aspectes sobre les característiques del llenguatge que interpreta JSBach.

---
El nostre doble intèrpret doncs realitza el control de les excepcions bàsiques que hi pot haver a qualsevol llenguatge de programació, com són:

- Divisió entre 0
- Crida a una variable no definida.
- Crida a un procediment no definit.
- Pas de parámetres incorrecte
- Accés a un índex inexistent d'una llista
- Eliminar un índex inexisteix d'una llista
- Redeclaració d'un procediment ja definit

Notem que cada cop que es detecti un dels possibles errors d'execució anteriors, una excepció indicant l'error s'imprimirà a la terminal, i es finalitzarà l'execució.

---
També cal aclarir la forma en la que podem inserir comentaris i és que es poden fer inserint: `~~~`al davant i al darrer del comentari que es vol fer. Per exemple:

    ~~~The Goldberg Variations és l'àlbum de debut del 1955 del pianista clàssic canadenc Glenn Gould. ~~~

---

Actualment, degut al disseny de la gramàtica, sempre es força l'existència d'un **Main** en el nostre programa. Aquesta restricció, es podria canviar si haguéssim canviat la forma de declarar el `root` de la gramàtica llevant el `main` i redefinint el *visitor* `root`. 

---

També la nostra gramàtica té en compte l'espai entre el condicional `if` i la condició `(a>b)` i l'espai entre aquesta condició i `|:` . A la vegada respecta els espais entre `a <- 5`. Un exemple:

    if a>b |:
        a <- 5
    :|

També és important comentar, que per un tema d'estil, s'ha optat per alhora de definir condicions fer-ho de forma en la que els operands i l'operador en les condicions: `if`, `if else` i `while` estiguin junts, tal i com es veu a l'exemple anterior: `a>b`

## Informació sobre els tests
Per poder provar la correcta funcionalitat d'aquest *doble intèrpret* s'ha executat aquest reguitzell d'exemples del llenguatge de programació JSBach:
* [test-halloBach.jsb](https://github.com/Martaw-code/Practica-LP/test-halloBach.jsb)
* [test-mcdEuclides.jsb](https://github.com/Martaw-code/Practica-LP/blob/main/test-mcdEuclides.jsb)
* [test-TorresDeHanoi.jsb](https://github.com/Martaw-code/Practica-LP/blob/main/test-TorresDeHanoi.jsb)
* [test-Suma.jsb](https://github.com/Martaw-code/Practica-LP/blob/main/test-Suma.jsb)
* [test-4OctaveScale.jsb](https://github.com/Martaw-code/Practica-LP/blob/main/test-4OctaveScale.jsb)

Se'n podrien afegir una pila més! Però aquests fitxers que comencen amb`test-*.jsb` en son un breu exemple de com podeu escriure les vostres pròpies  *Variacions Goldberg* o bé els programes que desitgeu.
## Referències
* [Transparències de l'assignatura de LP](https://gebakx.github.io/Python3/compiladors.html#)
* [Enunciat de la pràctica](https://github.com/jordi-petit/lp-jsbach-2022)
* [ANTLR4](https://www.antlr.org)
## Autor
Marta Granero i Martí - marta.granero.i@estudiantat.upc.edu
