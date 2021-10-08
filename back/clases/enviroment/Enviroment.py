from clases.enviroment.Simbol import *
class Enviroment:
    def __init__(self,antecesor,nombre):
        self.antecesor = antecesor
        self.variables = {}
        self.funciones = {}
        self.estructuras = {}
        self.nombre = nombre
        if antecesor == None:
            self.consola=""
            self.listaErrores=[]
            self.listaSimbolos = {}

    def getGlobal(self):
        entorno = self
        while entorno.antecesor != None:
            entorno = entorno.antecesor
        return entorno

    def findVariable(self,idVariable):
        entorno = self
        while entorno != None:
            if idVariable in entorno.variables.keys():
                return entorno.variables[idVariable]
            entorno = entorno.antecesor
        return None
    
    def findLocal(self,idVariable):
        entorno = self
        if idVariable in entorno.variables.keys():
            return entorno.variables[idVariable]
        return None
    
    def findGlobal(self,idVariable):
        entorno =self.getGlobal()
        if idVariable in entorno.variables.keys():
            return entorno.variables[idVariable]
        return None
    
    def add_variable(self,ide,valor,tipo,alcanse,fila=None,columna=None):
        '''
            alcance = 1 -> global \n
            alcance = 2 -> local \n
            alcance = 3 -> normal\n
        '''
        entorno = self
        nuevo = Simbolo(valor,ide,tipo,fila,columna)
        if alcanse == 3:
            if self.findVariable(ide) == None:
                self.variables[ide] = nuevo
                return
            else:
                self.modificar_variable(ide,valor,nuevo)
                return
        elif alcanse==2:
            entorno.variables[ide] = nuevo
        else:
            entorno = self.getGlobal()
            entorno.variables[ide]=nuevo

    def modificar_variable(self,identificador,valor,nuevo):
        env = self
        while env != None:
            if identificador in env.variables.keys():
                anterior:Simbolo = self.findVariable(identificador)
                # este es para modificar pero desde el compilador no del codigo de entrada
                nuevoaux = Simbolo(valor,anterior.simbolId,anterior.tipo,anterior.fila,anterior.columna)
                if nuevo != None:
                    env.variables[identificador] = nuevo
                else:
                    env.variables[identificador] = nuevoaux
                return
            else:
                env = env.antecesor

    def add_function(self,identificador,funcion):
        if identificador in self.funciones.keys():
            print('No se admiten funciones repetidas')
            
        else:
            self.funciones[identificador] = funcion 


    def get_fuction(self,identificador):
        env = self
        while env != None:
            if identificador in env.funciones.keys():
                return env.funciones[identificador]
            env = env.antecesor
        return None

    def addStruct(self,identificador,struct):
        if identificador in self.estructuras.keys():
            return False
        else:
            self.estructuras[identificador] = struct
            return True

    def getStruct(self, identidicador):
        env = self
        while env != None:
            if identidicador in env.estructuras.keys():
                return env.estructuras[identidicador]
            env = env.antecesor
        return None
            
    def addVariableStruct(self,identificador,tipoStruct,mut,atributos,alcance=None):
        env:Enviroment = self
        sim = Simbolo(None,identificador,Type.STRUCT,None,None,tipoStruct,mut)
        sim.atributos = atributos
        # quiere decir que es para una funcion
        if alcance == True:
            self.variables[identificador]=sim
            return
        while env != None:
            if identificador in env.variables.keys():
                env.variables[identificador]=sim
                return
            env = env.antecesor
        self.variables[identificador]=sim


            
