from clases.abstract.Expresion import Expresion
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator

class ExpresionLiteral(Expresion):
    def __init__(self,tipoDato,valorDato, line, column):
        Expresion.__init__(self,line,column)
        self.tipo=tipoDato # regresa el tipo de dato de la expresion
        self.valor=valorDato
    
    def compilar(self, enviroment):
        try:
            genAux = Generator()
            generator = genAux.getInstance()
            if (self.tipo==Type.INT or self.tipo==Type.FLOAT):
                return Return(self.valor,self.tipo)
            elif self.tipo == Type.BOOL:
                generator.addComent("Inicio Expresion Literal")
                if self.trueLb == '':
                    self.trueLb = generator.newLabel()
                if self.falseLb == '':
                    self.falseLb = generator.newLabel()

                if(self.valor):
                    generator.addGoto(self.trueLb)
                    generator.addComent("GOTO PARA EVITAR ERROR")
                    generator.addGoto(self.falseLb)
                else:
                    generator.addGoto(self.falseLb)
                    generator.addComent("GOTO PARA EVITAR ERROR")
                    generator.addGoto(self.trueLb)

                res = Return(self.valor, self.tipo, False)
                res.trueLb = self.trueLb
                res.falseLb = self.falseLb
                generator.addComent("Fin Expresion Literal")
                return res
            elif self.tipo == Type.STRING:
                generator.addComent("Inicio Expresion Literal")
                retorno = generator.addTemporal()
                generator.addExpresion('H','','',retorno)
                for caracter in str(self.valor):
                    generator.setHeap('H',ord(caracter))
                    generator.nextHeap()
                generator.setHeap('H',-1)
                generator.nextHeap()
                generator.setHeap('H',retorno)
                generator.nextHeap()
                generator.setHeap('H',-1)
                generator.nextHeap()
                generator.addComent("Fin Expresion Literal")
                return Return(retorno,Type.STRING,True)
            elif self.tipo == Type.CHAR:
                generator.addComent("Inicio Expresion Literal")
                generator.addComent("Fin Expresion Literal")
                return Return(ord(self.valor),Type.CHAR,False)

            else:
                print('falta culo')
        except:
            print('error en la expresion Literal')

