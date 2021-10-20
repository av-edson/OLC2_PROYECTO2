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
        self.diccionarioNativas = {}
        self.limpiarDirectorioNativas()

    def limpiarTodo(self):
        self.TempCont = 0
        self.LabelCont = 0

        self.codigo = ''
        self.funciones = ''
        self.natives = ''
        self.inFunc = False
        self.inNativas = False

        self.temps = []

        Generator.generator = Generator()
        self.limpiarDirectorioNativas()

    def limpiarDirectorioNativas(self):
        self.diccionarioNativas = {}
        self.diccionarioNativas["mathError"] = False
        self.diccionarioNativas["printString"] = False
        self.diccionarioNativas["mathMod"] = False
        self.diccionarioNativas["potencia"] = False
        self.diccionarioNativas["concatenarString"] = False
        self.diccionarioNativas["potenciaString"] = False
        self.diccionarioNativas["igualarString"] = False
        self.diccionarioNativas["upper"]=False
        self.diccionarioNativas["lower"]=False

    # ----------------------  OBTENER STATICO -------------------
    def getInstance(self):
        if Generator.generator == None:
            Generator.generator = Generator()
        return Generator.generator
    # ----------------------  CODIGO ----------------------------

    def getEncabezado(self):
        head = '/*----Encabezado----*/ \n package main; \n \n import (\n\t"fmt"\n'
        if self.diccionarioNativas["mathMod"]:
            head += '\t"math"\n'
        head += ")\n\n"
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

    def ingresarCodigo(self, codigo):
        if (self.inNativas):
            if(self.natives == ''):
                self.natives = self.natives + '/*-----NATIVES-----*/\n'
                self.natives = self.natives + codigo
            else:
                self.natives = self.natives + '\t' + codigo
        elif(self.inFunc):
            if(self.funciones == ''):
                self.funciones = self.ffuncionesuncs + '/*-----FUNCS-----*/\n'
            self.funciones = self.funciones + '\t' + codigo
        else:
            self.codigo = self.codigo + '\t' + codigo

    def addComent(self, comentario):
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
        self.LabelCont += 1
        return label

    def putLabel(self, label):
        self.ingresarCodigo(f'{label}:\n')
    # -------------------------- GOTO -----------------------------

    def addGoto(self, label):
        self.ingresarCodigo(f'goto {label};\n')
    # -------------------------- EXPRESIONES ----------------------

    def addExpresion(self, izquierdo, derecho, operacion, resultado):
        self.ingresarCodigo(f'{resultado}={izquierdo}{operacion}{derecho};\n')
    # -------------------------- INSTRUCCIONES --------------------

    def addPrint(self, tipo, valor):
        if str(tipo) == "f":
            self.ingresarCodigo(f'fmt.Printf("%{tipo}", float64({valor}));\n')
        else:
            self.ingresarCodigo(f'fmt.Printf("%{tipo}", int({valor}));\n')

    def printTrue(self):
        self.addPrint("c", 116)  # t
        self.addPrint("c", 114)  # r
        self.addPrint("c", 117)  # u
        self.addPrint("c", 101)  # e

    def printFalse(self):
        self.addPrint("c", 102)  # f
        self.addPrint("c", 97)  # a
        self.addPrint("c", 108)  # l
        self.addPrint("c", 115)  # s
        self.addPrint("c", 101)  # e

    def addComent(self, comentario):
        self.ingresarCodigo(f'/* {comentario} */\n')

    def addIf(self, izq, der, op, label):
        self.ingresarCodigo(f'if {izq} {op} {der} {{goto {label};}}\n')

    # ----------------------- FUNCIONES -------------------------
    def addInicioFuncion(self, ide):
        if(not self.inNativas):
            self.inFunc = True
        self.ingresarCodigo(f'func {ide}(){{\n')

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
    # -------------------------- STACK--------------------------

    def setStack(self, pos, value):
        self.ingresarCodigo(f'stack[int({pos})]={value};\n')

    def getStack(self, place, pos):
        self.ingresarCodigo(f'{place}=stack[int({pos})];\n')
    # ---------------------------- ENVS------------------------

    def newEnv(self, size):
        self.ingresarCodigo(f'P=P+{size};\n')

    def callFun(self, id):
        self.ingresarCodigo(f'{id}();\n')

    def retEnv(self, size):
        self.ingresarCodigo(f'P=P-{size};\n')
    # -------------------------- NATIVAS ---------------------------

    def funPrintString(self):
        if(self.diccionarioNativas["printString"]):
            return
        self.diccionarioNativas["printString"] = True
        self.inNativas = True

        self.addInicioFuncion("printString")
        # label salir funcion
        returnLb = self.newLabel()
        # label buscar fin de cadena
        compareLb = self.newLabel()
        # temporal heacp
        tempH = self.addTemporal()
        self.addExpresion('H','2','-',tempH)
        self.getHeap(tempH,tempH)

        # Temporal para comparar
        tempC = self.addTemporal()

        self.putLabel(compareLb)

        self.getHeap(tempC, tempH)
        #self.addExpresion('H', '1', '-', 'H')
        self.addIf(tempC, '-1', '==', returnLb)

        self.addPrint('c', tempC)

        self.addExpresion(tempH, '1', '+', tempH)

        self.addGoto(compareLb)

        self.putLabel(returnLb)
        self.addEndFuncion()
        self.inNativas = False

    def funPrintMathError(self):
        if(self.diccionarioNativas["mathError"]):
            return
        self.diccionarioNativas["mathError"] = True
        self.inNativas = True

        self.addInicioFuncion("mathError")
        # label salir funcion
        self.addPrint('c', 77)
        self.addPrint('c', 97)
        self.addPrint('c', 116)
        self.addPrint('c', 104)
        self.addPrint('c', 69)
        self.addPrint('c', 114)
        self.addPrint('c', 114)
        self.addPrint('c', 111)
        self.addPrint('c', 114)

        self.addEndFuncion()
        self.inNativas = False

    def activarModulo(self, izquierdo, derecho, resultado):
        self.diccionarioNativas["mathMod"] = True
        self.ingresarCodigo(f'{resultado}=math.Mod({izquierdo},{derecho});\n')

    def funPotencia(self):
        if(self.diccionarioNativas["potencia"]):
            return
        self.diccionarioNativas["potencia"] = True
        self.inNativas = True

        self.addInicioFuncion("potencia")
        # label salir funcion
        returnLb = self.newLabel()
        finPotencia = self.newLabel()

        contenidoBase = self.addTemporal()

        contenidoPotencia = self.addTemporal()

        # colocamos el puntero uno despues que es el stack del return
        self.addExpresion('P', '2', '-', 'P')
        self.getStack(contenidoBase, 'P')
        # siguiente puntero
        self.addExpresion('P', 1, '+', 'P')
        # recuperados valor de potencia del stack
        self.getStack(contenidoPotencia, 'P')

        tempComparacion = contenidoPotencia
        tempMulti = self.addTemporal()
        tempResultado = self.addTemporal()

        # valor que se multiplica
        self.addExpresion(contenidoBase, contenidoBase, "*", tempMulti)

        self.putLabel(finPotencia)
        self.addIf(tempComparacion, '1', '==', returnLb)
        # operaciones matematicas
        self.addExpresion(tempMulti, tempResultado, '+', tempResultado)
        self.addExpresion(contenidoPotencia, 1, '-', contenidoPotencia)
        self.addGoto(finPotencia)

        self.putLabel(returnLb)
        # puntero a lugar de return
        self.addExpresion('P', 2, '-', 'P')
        self.setStack('P', tempResultado)
        self.addEndFuncion()
        self.inNativas = False

    def funConcatenarString(self):
        if(self.diccionarioNativas["concatenarString"]):
            return
        self.diccionarioNativas["concatenarString"] = True
        self.inNativas = True
        self.addInicioFuncion("concatenarString")
        temp1 = self.addTemporal() # t2
        self.addExpresion('H', '3', '-', temp1)
        index1 = self.addTemporal() # t3
        self.getHeap(index1, temp1)
        tempReturn = self.addTemporal()
        self.addExpresion(index1,'','',tempReturn)

        temp2 = self.addTemporal() # t4
        self.addExpresion(temp1, '1', '+', temp2)
        index2 = self.addTemporal() # t5
        self.getHeap(index2, temp2)
        self.addExpresion(index1, '', '', 'H')

        returnLb = self.newLabel()
        recorrido1Lb = self.newLabel()
        recorrido2Lb = self.newLabel()

        self.putLabel(recorrido1Lb)
        iterador = self.addTemporal()
        self.getHeap(iterador, index1)
        self.addIf(iterador, '-1', '==', recorrido2Lb)

        self.setHeap('H', iterador)
        self.nextHeap()
        self.addExpresion(index1, '1', '+', index1)
        self.addGoto(recorrido1Lb)
        # recorrido del otro string
        self.putLabel(recorrido2Lb)
        self.getHeap(iterador, index2)
        self.addIf(iterador, '-1', '==', returnLb)
        self.setHeap('H', iterador)
        self.nextHeap()
        self.addExpresion(index2, '1', '+', index2)
        self.addGoto(recorrido2Lb)
        # return lb
        self.putLabel(returnLb)
        self.setHeap('H', '-1')
        self.nextHeap()
        self.setHeap('H',tempReturn)
        self.nextHeap()
        self.setHeap('H', '-1')
        self.nextHeap()
        #self.addExpresion('H','1','-','H')

        self.addEndFuncion()
        self.inNativas = False

    def funcPotenciaString(self):
        if self.diccionarioNativas["potenciaString"]:
            return
        self.inNativas = True
        self.diccionarioNativas["potenciaString"] = True

        self.addInicioFuncion("potenciaString")
        indexStack = self.addTemporal() # a4 
        self.addExpresion('H','3','-',indexStack)
        tempPalabra = self.addTemporal() # a2
        self.addExpresion(indexStack,'1','+',tempPalabra)
        indexPotencia = self.addTemporal() # a3
        self.getHeap(indexPotencia,tempPalabra) 
        self.addExpresion(indexPotencia,'1','+',indexPotencia)
        regreso = self.addTemporal() # a6
        self.getHeap(regreso,indexStack)

        # almacenando posicion en el regreso
        posicionRegreso = self.addTemporal() # a5
        self.addExpresion('H','','',posicionRegreso)

        # primer ciclo
        lbCiclo1 = self.newLabel()
        lblReturn = self.newLabel()
        lbCiclo2 = self.newLabel()
        # primer label
        self.putLabel(lbCiclo1)
        self.addExpresion(indexPotencia,'1','-',indexPotencia)
        iterador = self.addTemporal() # a0 
        self.getHeap(iterador,indexStack)
        self.addIf(indexPotencia,'0','==',lblReturn)
        self.addGoto(lbCiclo2)
        #segundo label
        self.putLabel(lbCiclo2)
        iterador2 = self.addTemporal()
        self.getHeap(iterador2,iterador)
        self.addIf(iterador2,'-1','==',lbCiclo1)
        self.setHeap('H',iterador2)
        self.nextHeap()
        self.addExpresion(iterador,'1','+',iterador)
        self.addGoto(lbCiclo2)
        # label return
        self.putLabel(lblReturn)
        self.setHeap('H','-1')
        #self.nextHeap()
        #self.setHeap('H',regreso)
        #self.nextHeap()
        #self.setHeap('H',posicionRegreso)
        #self.nextHeap()
        #self.setHeap('H','-1')
        #self.addExpresion('H','1','-','H')      
        #tempReturn = self.addTemporal()
        #self.addExpresion('P','1','+',tempReturn)
        #self.setStack(tempReturn,posicionRegreso)
        self.addExpresion(regreso,'','','H ')
        reescribir = self.newLabel()
        salida = self.newLabel()
        self.putLabel(reescribir)
        index = self.addTemporal()
        self.getHeap(index,posicionRegreso)
        self.addIf(index,'-1','==',salida)
        self.setHeap('H',index)
        self.nextHeap()
        self.addExpresion(posicionRegreso,'1','+',posicionRegreso)
        self.addGoto(reescribir)

        self.putLabel(salida)
        self.setHeap('H','-1')
        self.nextHeap()
        self.setHeap('H',regreso)
        self.nextHeap()
        self.setHeap('H','-1')
        self.nextHeap()
        #self.addExpresion('H','1','-','H')

        self.addEndFuncion()
        self.inNativas = False

