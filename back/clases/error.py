class Error():
    def __init__(self,descripcion,linea,columna,fecha):
        self.desc = str(descripcion)
        self.lin = str(linea)
        self.col=str(columna)
        self.fecha=str(fecha)