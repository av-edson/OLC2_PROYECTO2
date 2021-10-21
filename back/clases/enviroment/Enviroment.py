from clases.enviroment.Simbol import *
class Enviroment:
    def __init__(self,antecesor,nombre):
        self.antecesor = antecesor
        # NUEVO
        self.nombre = nombre
        self.size = 0
        self.lbBreack = ''
        self.lbContinue = ''
        self.lbReturn = ''
        if(antecesor != None):
            self.size = self.antecesor.size
            self.lbContinue = self.antecesor.lbContinue
            self.lbBreack = self.antecesor.lbBreack
            self.lbReturn = self.antecesor.lbReturn
        
        self.variables = {}
        self.functions = {}
        self.structs = {}

    def getGlobal(self):
        env = self
        while env.antecesor != None:
            env = env.antecesor
        return env

    def sabeVar(self,id,tipo,inHeap,tipoStrct=None,esGlobal=None):
        globalAux = self.antecesor==None
        if esGlobal is not None:
            globalAux = globalAux or esGlobal
        if id in self.variables.keys():
            print("la variable ya existe")
        else:
            nuevoSimbolo = Simbolo(id,tipo,self.size,globalAux,inHeap,tipoStrct)
            self.size+=1
            self.variables[id]=nuevoSimbolo
        return self.variables[id]

    def saveFuncion(self, id, funcion):
        if id in self.functions.keys():
            print("Función repetida")
        else:
            self.functions[id] = funcion
            
    def getVariable(self, id,alcance=None):
        entorno = self
        if alcance:
            entorno = self.getGlobal()
            if id in entorno.variables.keys():
                return entorno.variables[id]
            return None
        elif alcance is None:
            while entorno != None:
                if id in entorno.variables.keys():
                    return entorno.variables[id]
                entorno = entorno.antecesor
            return None
        elif alcance is False:
            if id in entorno.variables.keys():
                    return entorno.variables[id]
            return None
    
    def getFuncion(self, id):
        entorno = self
        while entorno != None:
            if id in entorno.functions.keys():
                return entorno.functions[id]
        return None