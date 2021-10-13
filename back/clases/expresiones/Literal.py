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
                return res
            elif self.tipo == Type.STRING:
                retorno = generator.addTemporal()
                generator.addExpresion('H','','',retorno)
                for caracter in str(self.valor):
                    generator.setHeap('H',ord(caracter))
                    generator.nextHeap()
                generator.setHeap('H',-1)
                generator.nextHeap()
                return Return(retorno,Type.STRING,True)


            else:
                print('falta culo')
        except:
            print('error en la expresion Literal')

