from antlr4 import *
from jsbachLexer import jsbachLexer
from jsbachParser import jsbachParser
import sys
import os

if __name__ is not None and "." in __name__:
    from .jsbachVisitor import jsbachVisitor
else:
    from jsbachVisitor import jsbachVisitor

#-------SECCIÓ PER GENERAR EL FITXER LILY-------#

def lilyNota(nota):
    baseToNota = {
        -5: 'c',
        -4: 'd',
        -3: 'e',
        -2: 'f',
        -1: 'g',
        0:  'a',
        1:  'b'
    }

    nombreNota = ((nota+5) % 7)-5
    notaReal = baseToNota[nombreNota]
    octava = int((nota-nombreNota)/7)
    resultat = notaReal

    for i in range(octava, 3, +1):
        resultat += ","

    for i in range(octava, 3, -1):
        resultat += "'"

    return resultat + " "


def notesToString(notes):
    n = ""
    for nota in notes:
        n += lilyNota(nota)
    return n


def fitxerLily(notes):
    return """\\version "2.22.1"
\\score {
    \\absolute {
        \\tempo 4 = 120
        %s
    }
    \\layout { }
    \\midi { }
}""" % (notesToString(notes))


notaToBase = {
    'C': -5,
    'D': -4,
    'E': -3,
    'F': -2,
    'G': -1,
    'A': 0,
    'B': 1
}


def noteToInt(textNota):
    nota = textNota[0]
    octava = 4
    if len(textNota) > 1:
        octava = int(textNota[1])
    noteInt = notaToBase[nota]
    return noteInt + octava*7

#-----------------------------------------------#


def suma(x1, x2):
    return x1 + x2


def resta(x1, x2):
    return x1 - x2


def mul(x1, x2):
    return x1 * x2


def div(x1, x2):
    if x2 == 0:
        raise Exception("DIVISON BY ZERO")
    else:
        return x1 / x2


def mod(x1, x2):
    return x1 % x2


diccionari = {'+': suma, '-': resta, '*': mul, '/': div, '%': mod}


def eq(x1, x2):
    return x1 == x2


def lt(x1, x2):
    return x1 < x2


def gt(x1, x2):
    return x1 > x2


def neq(x1, x2):
    return x1 != x2


def lte(x1, x2):
    return x1 <= x2


def gte(x1, x2):
    return x1 >= x2


condicions = {
    '==': eq, '<': lt, '>': gt, '/=': neq,
    '<=': lte, '>=': gte
}


class BachVisitor(jsbachVisitor):
    def __init__(self):
        self.simbols = [{}]

        self.parFuncions = {}
        self.codiFuncions = {}

        self.aux = 0
        self.fun = "null"
        self.para = []

        self.parametres = []
        self.totsProcediments = {}

        self.notes = []

    def executa(self, root, funcio, par):
        if funcio != "null":
            self.fun = funcio
            self.para = par
            self.parametres = par
        self.visit(root)
        return self.notes

    # VISITOR DE ROOT

    def visitRoot(self, ctx):
        l = list(ctx.getChildren())
        j = 0
        aux = 0
        while j < len(l) - 1:
            if isinstance(l[j], jsbachParser.MainContext):
                aux = j
            else:
                self.visit(l[j])
                print(l[j].getText())
            j = j+1

        if self.fun != "null":
            par = {}
            par2 = self.parFuncions[self.fun]
            par3 = self.para
            if len(par2) != len(par3):
                raise Exception("PARAMETERS DO NOT MATCH")

            j = 0
            while j < len(par3):
                par[par2[j]] = par3[j]
                j = j + 1

            self.simbols.append(par)
            funcions = self.codiFuncions[self.fun]
            for f in funcions:
                self.visit(f)
            self.simbols.pop()

        self.visit(l[aux])

    # VISITOR D'EXPRESSIÓ #

    def visitExpr(self, ctx):
        l = list(ctx.getChildren())
        valor = l[0].getText()

        if ctx.NUM():
            return int(ctx.getText())
        elif ctx.llargada():
            return self.visit(ctx.llargada())
        elif ctx.consulta():
            return self.visit(ctx.consulta())
        elif ctx.NOTA():
            return noteToInt(ctx.getText())
        elif ctx.VAR():
            if not(valor in self.simbols[-1]):
                raise Exception("VARIABLE " + valor + " NOT DEFINED")
            return self.simbols[-1][valor]
        else:  # expressions de suma i la resta d'operacioons
            if l[0].getText() == "(":
                return self.visit(l[1])

            else:
                return diccionari[l[1].getText()](self.visit(l[0]),
                                                  self.visit(l[2]))

    # VISITORS D'INSTRUCCIONS BÀSIQUES #

    def visitAssignacio(self, ctx):
        l = list(ctx.getChildren())
        var = l[0].getText()

        if ctx.expr():
            self.simbols[-1][var] = self.visit(l[2])

        elif ctx.llista():
            self.simbols[-1][var] = self.visit(l[2])

    def visitReproduccio(self, ctx):
        l = list(ctx.getChildren())
        if ctx.expr():
            self.notes.append(self.visit(ctx.expr()))
        else:
            self.notes.extend(self.visit(ctx.llista()))

    def visitLectura(self, ctx):
        l = list(ctx.getChildren())
        var = l[1].getText()
        self.simbols[-1][var] = int(input())

    def visitBlocText(self, ctx):
        s = ctx.getText()[1:-1]
        return s

    def visitEscriptura(self, ctx):
        l = list(ctx.getChildren())

        for e in l[2::2]:
            if e != " ":
                print(self.visit(e), end="")
        print("")

    # VISITOR DE LES DIFERENTES INSTRUCCIONS #

    def visitInstruction(self, ctx):
        for i in list(ctx.getChildren()):
            self.visit(i)

    # VISITORS DE CONDICIONALS #

    def visitCondicionalIf(self, ctx):
        l = list(ctx.getChildren())
        x1 = self.visit(l[2])
        x2 = self.visit(l[4])
        i = 7
        if condicions[l[3].getText()](x1, x2):
            while l[i].getText() != ":|":
                self.visit(l[i])
                i = i + 1

    def visitCondicionalIfElse(self, ctx):
        l = list(ctx.getChildren())
        x1 = self.visit(l[2])
        x2 = self.visit(l[4])
        i = 7
        if condicions[l[3].getText()](x1, x2):
            while l[i].getText() != ":|":
                self.visit(l[i])
                i = i + 1

        else:
            while l[i].getText() != "|:":
                i = i + 1

            while l[i].getText() != ":|":
                self.visit(l[i])
                i = i + 1

    def visitLoopWhile(self, ctx):
        l = list(ctx.getChildren())
        x1 = self.visit(l[2])
        x2 = self.visit(l[4])

        while condicions[l[3].getText()](x1, x2):
            for i in range(7, len(l) - 1):
                self.visit(l[i])
            x1 = self.visit(l[2])
            x2 = self.visit(l[4])

    # VISITORS DE PROCEDIMENTS #

    def visitCjtVar(self, ctx):
        l = list(ctx.getChildren())
        par = []
        for c in l:
            if c.getText() != " ":
                if c.getText() in par:
                    raise Exception("PARAMETER " + c.getText() +
                                    " ALREADY IN THE FUNCTION")
                par.append(c.getText())

        return par

    def visitDeclaraFuncio(self, ctx):
        if ctx.FUNC().getText() in self.totsProcediments:
            raise Exception('FUNCTION ' +
                            ctx.FUNC().getText() +
                            'ALREADY DEFINED')
        else:
            parametresProcediment = []
            z = 2
            while ctx.getChild(z).getText() != '|:':
                if ctx.getChild(z).getText() != ' ':
                    if ctx.getChild(z).getText() in parametresProcediment:
                        raise Exception('ON THE DEFINITION OF THE FUNCTION ' +
                                        ctx.FUNC().getText()
                                        + 'EXISTS MULTIPLE PARAMETERS WITH SAME NAME')
                    else:
                        parametresProcediment.append(ctx.getChild(z).getText())
                z += 1
            llistaAAfegir = [ctx.instruction(), parametresProcediment]
            self.totsProcediments[ctx.FUNC().getText()] = llistaAAfegir

    def visitCridaProc(self, ctx):
        valorsparametres = []

        for expr in ctx.expr():
            valorsparametres.append(self.visit(expr))
        self.executaProcediment(ctx.FUNC().getText(), valorsparametres)

    def executaProcediment(self, nomProcediment, parametresProcediment):
        if nomProcediment not in self.totsProcediments:
            raise Exception('FUNCTION ' + nomProcediment +
                            'IS NOT DEFINED')
        else:
            if len(self.totsProcediments[nomProcediment][1]) \
                    != len(parametresProcediment):
                raise Exception('NUMBER OF PARAMETERS DO NOT MATCH' +
                                nomProcediment)
            else:
                variablesAfegir = {}

                for nomParametre, valorParametre in \
                        zip(self.totsProcediments[nomProcediment][1],
                            parametresProcediment):
                    variablesAfegir[nomParametre] = valorParametre
                self.simbols.append(variablesAfegir)

                for ins in self.totsProcediments[nomProcediment][0]:
                    self.visit(ins)
                self.simbols.pop()

    # VISITORS DE LLISTES #

    def visitLlista(self, ctx):
        par = []
        for expr in ctx.expr():
            par.append(self.visit(expr))
        return par

    def visitConsulta(self, ctx):
        l = list(ctx.getChildren())
        t = self.simbols[-1][l[0].getText()]
        pos = self.visit(l[2])
        if pos >= len(t):
            raise Exception("INDEX OUT OF BOUNDS")
        return (t[pos])

    def visitLlargada(self, ctx):
        l = list(ctx.getChildren())
        t = self.simbols[-1][l[1].getText()]
        if (len(t) == 0):
            raise Exception("EMPTY LIST")
        return len(t)

    def visitAfegeix(self, ctx):
        l = list(ctx.getChildren())
        elem = self.visit(l[4])
        self.simbols[-1][l[0].getText()].append(elem)

    def visitElimina(self, ctx):
        l = list(ctx.getChildren())
        t = self.simbols[-1][l[2].getText()]
        pos = self.visit(l[4])
        if pos >= len(t):
            raise Exception("INDEX OUT OF BOUNDS")
        t.pop(pos)

    def visitMain(self, ctx):
        l = list(ctx.getChildren())
        i = 3

        while i < len(l)-1:
            self.visit(l[i])
            i = i + 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('PARÀMETRES INSUFICIENTS')

    input_stream = FileStream(sys.argv[1], 'utf-8')

    i = 2
    fun = "null"
    par = []
    while i < len(sys.argv):
        if i == 2:
            fun = sys.argv[i]
        else:
            par.append(int(sys.argv[i]))
        i = i + 1

    lexer = jsbachLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = jsbachParser(token_stream)
    tree = parser.root()

    # print(tree.toStringTree(recog=parser))

    visitor = BachVisitor()
    notes = visitor.executa(tree, fun, par)

    print("Musiknoten: ", notes)

    if len(notes) == 0:
        print("EL TEU FITXER NO CONTÉ MUSIKNOTEN!")
        sys.exit()

    filename = "output"
    fitxerlily = fitxerLily(notes)

    with open(filename + ".lily", 'w') as f:
        f.write(fitxerlily)
    print("")

    os.system("lilypond " + filename + ".lily")
    os.system("timidity -Ow -o " + filename + ".wav " + filename + ".midi")
    os.system("ffmpeg -i " + filename +
              ".wav -codec:a libmp3lame -qscale:a 2 " + filename + ".mp3")
