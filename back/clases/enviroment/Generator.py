from .Enviroment import Enviroment

class Generator:
    generator = None
    def __init__(self):
        self.TempCont = 0
        self.LabelCont = 0

        self.codigo = ''
        self.funciones = ''
        self.natives = ''
        self.inFunc = False
        self.inNativas = False

        self.temps = []

        self.printString = False

    def limpiarTodo(self):
        self.TempCont = 0
        self.LabelCont = 0

        self.codigo = ''
        self.funciones = ''
        self.natives = ''
        self.inFunc = False
        self.inNativas = False

        self.temps = []

        self.printString = False
        Generator.generator = Generator() 

    # ----------------------  OBTENER STATICO -------------------
    def getInstance(self):
        if Generator.generator == None:
            Generator.generator = Generator()
        return Generator.generator
    # ----------------------  CODIGO ----------------------------
    def getEncabezado(self):
        head= '/*----Encabezado----*/ \n package main; \n \n import (\n\t"fmt"\n)\n\n'
        if len(self.temps) > 0:
            head += 'var '
            for temp in range(len(self.temps)):
                head += self.temps[temp]
                if temp != (len(self.temps) - 1):
                    head += ","
            head += " float64\n"
        head += "var P, H float64;\nvar stack [30101999]float64;\nvar heap [30101999]float64;\n\n"
        return head
    
    def getCodigo(self):
        aux = f'{self.getEncabezado()}{self.natives}\n{self.funciones}\nfunc main(){{\n{self.codigo}\n}}'
        return aux

    def ingresarCodigo(self,codigo):
        if (self.inNativas):
            if(self.natives == ''):
                self.natives = self.natives + '/*-----NATIVES-----*/\n'
            self.natives = self.natives + '\t' + codigo
        elif(self.inFunc):
            if(self.funciones == ''):
                self.funciones = self.ffuncionesuncs + '/*-----FUNCS-----*/\n'
            self.funciones = self.funciones + '\t' +  codigo
        else:
            self.codigo = self.codigo + '\t' +  codigo
    
    def addComent(self,comentario):
        self.ingresarCodigo(f'/*{comentario}*/\n')
    
    # -------------------------- TEMPORALES -----------------------
    def addTemporal(self):
        temp = f't{self.TempCont}'
        self.TempCont += 1
        self.temps.append(temp)
        return temp
    # -------------------------- EXPRESIONES ----------------------
    def addExpresion(self,izquierdo,derecho,operacion,resultado):
        self.ingresarCodigo(f'{resultado}={izquierdo}{operacion}{derecho};\n')
    # -------------------------- INSTRUCCIONES --------------------
    def addPrint(self,tipo,valor):
        if valor==None:
            self.ingresarCodigo(f'fmt.Print("\\n");\n')
        else:
            self.ingresarCodigo(f'fmt.Printf("%{tipo}", int({valor}));\n')
