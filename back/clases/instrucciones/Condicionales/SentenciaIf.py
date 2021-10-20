from clases.abstract.Instruccion import Instruccion
from clases.abstract.Return import Return, Type
from clases.enviroment.Generator import Generator

class If(Instruccion):

    def __init__(self,expresion,instruccioens, line, column,elseST=None):
        Instruccion.__init__(self,line, column)
        self.expresion = expresion
        self.instrucciones = instruccioens
        self.elseST = elseST
    
    def compilar(self, enviroment):
        genAux = Generator()
        generator = genAux.getInstance()

        generator.addComent("Inicio sentencia If")
        expresion:Return = self.expresion.compilar(enviroment)

        if expresion.tipo != Type.BOOL:
            print('La expresion del if no es booleana')
            generator.addComent("Fin sentencia If")
            return
        
        generator.putLabel(expresion.trueLb)
        
        self.instrucciones.compilar(enviroment)

        if self.elseST != None:
            ifSalida = generator.newLabel()
            generator.addGoto(ifSalida)
        
        generator.putLabel(expresion.falseLb)
        if self.elseST != None:
            self.elseST.compilar(enviroment)
            generator.putLabel(ifSalida)
        
        generator.addComent("Fin sentencia If")
        return
