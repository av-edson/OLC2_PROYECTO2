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
    # -------------------------- LABELS ---------------------------
    def newLabel(self):
        label = f'L{self.LabelCont}'
        self.LabelCont+=1
        return label
    
    def putLabel(self,label):
        self.ingresarCodigo(f'{label}:\n')
    # -------------------------- GOTO -----------------------------
    def addGoto(self,label):
        self.ingresarCodigo(f'goto {label};\n')
    # -------------------------- EXPRESIONES ----------------------
    def addExpresion(self,izquierdo,derecho,operacion,resultado):
        self.ingresarCodigo(f'{resultado}={izquierdo}{operacion}{derecho};\n')
    # -------------------------- INSTRUCCIONES --------------------
    def addPrint(self,tipo,valor):
        if str(tipo)=="f":
            self.ingresarCodigo(f'fmt.Printf("%{tipo}", float64({valor}));\n')
        else:
            self.ingresarCodigo(f'fmt.Printf("%{tipo}", int({valor}));\n')
    
    def printTrue(self):
        self.addPrint("c", 116) #t
        self.addPrint("c", 114) #r
        self.addPrint("c", 117) #u
        self.addPrint("c", 101) #e

    def printFalse(self):
        self.addPrint("c", 102) #f
        self.addPrint("c", 97)  #a
        self.addPrint("c", 108) #l
        self.addPrint("c", 115) #s
        self.addPrint("c", 101) #e
    
    def addComent(self,comentario):
        self.ingresarCodigo(f'/* {comentario} */\n')
    
    def addIf(self,izq,der,op,label):
        self.ingresarCodigo(f'if {izq} {op} {der} {{goto {label};}}\n')

    #----------------------- FUNCIONES -------------------------
    def addInicioFuncion(self, ide):
        if(not self.inNativas):
            self.inFunc = True
        self.ingresarCodigo(f'func {ide}(){{\n', '')
    
    def addEndFuncion(self):
        self.ingresarCodigo('return;\n}\n')
        if(not self.inNativas):
            self.inFunc = False
    # -------------------------- HEAP ------------------
    def setHeap(self, pos, value):
        self.ingresarCodigo(f'heap[int({pos})]={value};\n')

    def getHeap(self, place, pos):
        self.ingresarCodigo(f'{place}=heap[int({pos})];\n')

    def nextHeap(self):
        self.ingresarCodigo('H=H+1;\n')
    #-------------------------- STACK--------------------------
    def setStack(self, pos, value):
        self.ingresarCodigo(f'stack[int({pos})]={value};\n')
    
    def getStack(self, place, pos):
        self.ingresarCodigo(f'{place}=stack[int({pos})];\n')
    # -------------------------- NATIVAS ---------------------------
    def funPrintString(self):
        if(self.printString):
            return
        self.printString = True
        self.inNativas=True

        self.addInicioFuncion("printString")
        # label salir funcion
        returnLb = self.newLabel()
        # label buscar fin de cadena
        compareLb = self.newLabel()
        # temporal puntero stack
        tempP = self.addTemporal()
        # temporal heacp
        tempH = self.addTemporal()

        self.addExpresion('P',1,'+',tempP)
        self.getStack(tempH, tempP)

        # Temporal para comparar
        tempC = self.addTemporal()

        self.putLabel(compareLb)

        self.getHeap(tempC, tempH)

        self.addIf(tempC, '-1', '==', returnLb)

        self.addPrint('c', tempC)

        self.addExpresion(tempH, '1', '+',tempH)

        self.addGoto(compareLb)

        self.putLabel(returnLb)
        self.addEndFuncion()
        self.inNatives = False
