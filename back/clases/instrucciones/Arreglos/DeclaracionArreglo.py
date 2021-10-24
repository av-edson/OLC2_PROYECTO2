from clases.abstract.Expresion import *
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator
from clases.expresiones.Literal import ExpresionLiteral

class DeclaracionArreglo(Expresion):
    def __init__(self,expresiones, line, column,tipoAux=None):
        Expresion.__init__(self,line, column)
        self.expresiones = expresiones
        self.size = len(expresiones)
        self.tipoAux = tipoAux

    def compilar(self, enviroment):
        try:
            genAux = Generator()
            generator = genAux.getInstance()

            listaValores = []
            for expre in self.expresiones:
                if isinstance(expre,ExpresionLiteral):
                    if expre.tipo==Type.BOOL:
                        if expre.valor:
                            ret = Return(1,Type.BOOL)
                        else:
                            ret = Return(0,Type.BOOL)
                    else:
                        ret:Return = expre.compilar(enviroment)
                else: ret:Return = expre.compilar(enviroment)
                if ret is None:
                    print("expresion dentro de arreglo arrojo Nono")
                    generator.addExpresion('H','1','-','H')
                    return Return()
                if ret.tipo == Type.UNDEFINED or ret.tipo==Type.RETURNST or ret.tipo==Type.BREACKST or ret.tipo==Type.CONTINUEST:
                    print("Una de las expresiones del arreglo tiene error o no se admite")
                    generator.addExpresion('H','1','-','H')
                    return Return()
                listaValores.append(ret)


            tempRetorno = generator.addTemporal()
            generator.addExpresion('H','','',tempRetorno)
            generator.setHeap('H',self.size)
            generator.nextHeap()

            tipo = None
            for valor in listaValores:
                tipo = valor.tipo
                generator.setHeap('H',valor.valor)
                generator.nextHeap()

            return  Return(tempRetorno,Type.ARRAY,True,tipo)

        except:
            print("Ocurrio un error en la declaracion de arreglo")
