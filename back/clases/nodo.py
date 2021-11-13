class Nodo:
    
    def __init__(self,valor) -> None:
        self.valor = valor
        self.hijos = []
        self.contador = 0
        self.grafo = ""
    
    def ingresarHijo(self,hijo):
        self.hijos.append(hijo)
    
    def getGrafico(self) -> str:
        self.grafo = "digraph Tree{\n"
        self.grafo += "nodo0[label=\""+str(self.valor)+"\"];\n"
        self.contador = 1
        self.__graficar("nodo0",self)
        self.grafo += "}"
        return self.grafo

    def __graficar(self,padre:str,node):
        for hijo in node.hijos: 
            if hijo != None:
                nombre:str = "nodo"+str(self.contador)
                self.grafo += nombre + "[label=\""+str(hijo.valor)+"\"];\n"
                self.grafo += padre +" -> "+ nombre + ";\n"
                self.contador += 1
                self.__graficar(nombre,hijo) 
        return