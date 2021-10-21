from clases.abstract.Expresion import Expresion
from clases.abstract.Return import Return, Type
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator
from clases.instrucciones.Funciones.Funcion import Funcion
from clases.instrucciones.Funciones.Parametro import Parametro

class LLamadaFuncion(Expresion):
    def __init__(self,id,listaExpresiones, line, column):
        Expresion.__init__(self,line, column)
        self.id = id 
        self.expresiones = listaExpresiones

    def compilar(self, enviroment:Enviroment):
        try:
            funcion:Funcion = enviroment.getFuncion(self.id)
            if funcion !=None:
                valoresParametro = []
                aux = Generator()
                generador = aux.getInstance()
                size = enviroment.size

                valoresParametro = self.validarFuncion(enviroment,funcion)
                if valoresParametro != None:
                    regreso = generador.addTemporal()

                    generador.addExpresion('P', size+1, '+',regreso)

                    aux = 0
                    for param in valoresParametro:
                        aux = aux +1
                        generador.setStack(regreso, param.valor)
                        if aux != len(valoresParametro):
                            generador.addExpresion(regreso, '1', '+',regreso)

                    generador.newEnv(size)
                    generador.callFun(self.id)
                    generador.getStack(regreso, 'P')
                    generador.retEnv(size)

                    if funcion.tipo != None:
                        return Return(regreso, funcion.tipo, True)
                else: return Return()

            else:
                print("No se ha definico la funcon")
                return Return()
        except:
            print("Ocurrio un error al llamar a la funcion "+str(self.id))

    def validarFuncion(self,enviroment,funcion:Funcion):
        listaRegreso = []
        # compilando las expresiones y validando que no contengan errores
        for expre in self.expresiones:
            ret:Return = expre.compilar(enviroment)
            if ret.tipo == Type.UNDEFINED:
                print('Una expresion que envio como parametro contiene error en la funcion')
                return None
            else: listaRegreso.append(ret)
        
        if len(listaRegreso) != len(funcion.parametros): 
            print('numero de parametros que envio no coicide con el definido')
            return None

        for i in range(len(self.expresiones)):
            expre:Return = listaRegreso[i]
            param:Parametro = funcion.parametros[i]
            if expre.tipo != param.tipo:
                if param.tipo != None:
                    print('Un tipo de dato no coicide')
                    None
        return listaRegreso
