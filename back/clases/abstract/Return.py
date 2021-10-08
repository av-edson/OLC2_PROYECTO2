from enum import Enum

class Type(Enum):
    INT=0
    FLOAT=1
    STRING=2
    CHAR=3
    BOOL=4
    ARRAY=5
    NULO=6
    STRUCT=11
    
    UNDEFINED=7

    RETURNST=8
    BREACKST=9
    CONTINUEST=10
    
class Return:
    def __init__(self,value=0,tipo=Type.UNDEFINED,esTemp=False,tipoAux=""):
        self.valor=value
        self.tipo=tipo
        self.tipoAux = tipoAux
        self.esTemp = esTemp
        self.trueLb = ''
        self.falseLb = ''
