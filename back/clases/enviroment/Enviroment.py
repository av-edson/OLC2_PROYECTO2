import time
from clases.enviroment.Generator import Generator
from clases.enviroment.Simbol import *
from clases.error import Error
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

    def sabeVar(self,id,tipo,inHeap,tipoStrct=None,esGlobal=None,tipoAux=None):
        globalAux = self.antecesor==None
        if esGlobal is not None:
            globalAux = globalAux or esGlobal
        if id in self.variables.keys():
            genAux = Generator()
            generador = genAux.getInstance()
            generador.listaErrores.append(Error("La variable "+str(id)+" ya existe",0,0,str(time.strftime("%c")) ))
        else:
            if tipoAux != None:
                if tipoAux==Type.ARRAY:
                    nuevoSimbolo = Simbolo(id,tipo,self.size,globalAux,inHeap,tipoAux,tipoStrct)
                else:
                    nuevoSimbolo = Simbolo(id,tipo,self.size,globalAux,inHeap,tipoAux)
            else:
                nuevoSimbolo = Simbolo(id,tipo,self.size,globalAux,inHeap,tipoStrct)
            self.size+=1
            self.variables[id]=nuevoSimbolo
        return self.variables[id]

    def saveFuncion(self, id, funcion):
        if id in self.functions.keys():
            genAux = Generator()
            print("aca")
            generador = genAux.getInstance()
            generador.listaErrores.append(Error("No se admiten funciones repetidas",0,0,str(time.strftime("%c")) ))
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
    
    def saveStruct(self, id, struct):
        if id in self.structs.keys():
            print("Struct repetido")
        else:
            self.structs[id] = struct

    def getFuncion(self, id):
        entorno = self
        while entorno != None:
            if id in entorno.functions.keys():
                return entorno.functions[id]
            entorno =   entorno.antecesor
        return None