from clases.abstract.Instruccion import Instruccion

class BloqueInstrucciones(Instruccion):
    def __init__(self, listaInstrucciones,line, column):
        Instruccion.__init__(self,line, column)
        self.listaInstrucciones = listaInstrucciones

    def compilar(self, enviroment):
        try:
            for inst in self.listaInstrucciones:
                reg = inst.compilar(enviroment)
                if reg != None:
                    return reg
        except:
            print("error inesperado al ejecutar bloque de instrucciones")