from abc import ABC, abstractmethod

class Instruccion(ABC):
    def __init__(self,line,column):
        self.line = line
        self.column = column

    @abstractmethod
    def compilar(self,enviroment):
        pass