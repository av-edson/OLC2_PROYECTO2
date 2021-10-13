from clases.enviroment.Simbol import *
class Enviroment:
    def __init__(self,antecesor,nombre):
        self.antecesor = antecesor
        # NUEVO
        self.size = 0
        if(antecesor != None):
            self.size = self.antecesor.size
        
        self.variables = {}
        self.functions = {}
        self.structs = {}

    def getGlobal(self):
        env = self
        while env.antecesor != None:
            env = env.antecesor
        return env



            
