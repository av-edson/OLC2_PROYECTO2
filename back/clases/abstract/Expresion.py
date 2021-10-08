from abc import ABC,abstractmethod

class Expresion(ABC):
    def __init__(self,line,column):
        self.line=line
        self.column=column
        self.trueLb = ''
        self.falseLb = ''
    
    @abstractmethod
    def compilar(self,enviroment):
        pass