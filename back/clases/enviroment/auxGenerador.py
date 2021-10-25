from clases.enviroment.Generator import Generator

class auxGenerador:
    def __init__(self):
        aux = Generator()
        self.ge = aux.getInstance()
    
    def CompararString(self,op):
        if self.ge.diccionarioNativas["igualarString"]:
            return
        self.ge.diccionarioNativas["igualarString"]=True
        self.ge.inNativas = True

        self.ge.addInicioFuncion("igualarString")

        labelCiclo = self.ge.newLabel()
        labelAux = self.ge.newLabel()
        labelTrue = self.ge.newLabel()
        labelFalse = self.ge.newLabel()
        labelReturn = self.ge.newLabel()

        tempAux1 = self.ge.addTemporal()            # a0
        self.ge.addExpresion('H','3','-',tempAux1)  # a0 = H-3
        index1 = self.ge.addTemporal()              #a1
        self.ge.getHeap(index1,tempAux1)            # a1 = heap[a0]

        tempAux2 = self.ge.addTemporal()            # a2
        self.ge.addExpresion(tempAux1,'1','+',tempAux2)  # a2 = a0+1
        index2 = self.ge.addTemporal()              #a3
        self.ge.getHeap(index2,tempAux2)            # a3 = heap[a2]
        self.ge.addGoto(labelCiclo)             #goto L0

        self.ge.putLabel(labelCiclo)            # L0:
        palabra1 = self.ge.addTemporal()            #a4
        palabra2 = self.ge.addTemporal()            #a5
        self.ge.getHeap(palabra1,index1)            #a4=heap[a1]
        self.ge.getHeap(palabra2,index2)            #a5=heap[a3]

        self.ge.addIf(palabra1,'-1','==',labelAux)      #if a4 ==-1{goto L3}
        self.ge.addIf(palabra1,palabra2,op,labelFalse)  #if a4 != a5 {goto L1}

        self.ge.addExpresion(index1,'1','+',index1)     #a1=a1+1
        self.ge.addExpresion(index2,'1','+',index2)     #a3=a3+1
        self.ge.addGoto(labelCiclo)                     #goto L0;

        self.ge.putLabel(labelAux)                      #L3
        self.ge.addIf(palabra2,'-1','==',labelTrue)     #if a5 == -1 {goto L2}
        self.ge.addGoto(labelFalse)                     #goto L1

        self.ge.putLabel(labelFalse)                    #L1
        self.ge.setHeap('H','0')                        #heap[int(H)]=0
        self.ge.addGoto(labelReturn)                    #goto L4;

        self.ge.putLabel(labelTrue)                     #L2:
        self.ge.setHeap('H','1')                        #heap[int(H)]=1
        self.ge.addGoto(labelReturn)                    #goto L4;

        self.ge.putLabel(labelReturn)                   #L4:
        self.ge.nextHeap()                              #H=H+1;
        self.ge.setHeap('H','-1')                       #heap[int(H)]=-1;
        self.ge.nextHeap()                              #H=H+1;

        self.ge.addEndFuncion()
        self.ge.inNativas = False

    def Upper(self):
        if self.ge.diccionarioNativas["upper"]:
            return
        self.ge.diccionarioNativas["upper"]=True
        self.ge.inNativas=True
        self.ge.addInicioFuncion("upper")

        index = self.ge.addTemporal()
        self.ge.addExpresion('H','2','-',index)
        self.ge.getHeap(index,index)
        self.ge.addExpresion(index,'1','-',index)

        labelCiclo = self.ge.newLabel()
        labelAux = self.ge.newLabel()
        labelUpper = self.ge.newLabel()
        labelReturn = self.ge.newLabel()
        self.ge.addGoto(labelCiclo)
        self.ge.putLabel(labelCiclo)

        self.ge.addExpresion(index,'1','+',index)
        palabra = self.ge.addTemporal()
        self.ge.getHeap(palabra,index)
        self.ge.addIf(palabra,'-1','==',labelReturn)
        self.ge.addIf(palabra,'123','<',labelAux)
        self.ge.addGoto(labelCiclo)

        self.ge.putLabel(labelAux)
        self.ge.addIf(palabra,'96','>',labelUpper)
        self.ge.addGoto(labelCiclo)

        self.ge.putLabel(labelUpper)
        self.ge.addExpresion(palabra,'32','-',palabra)
        self.ge.setHeap(index,palabra)
        self.ge.addGoto(labelCiclo)

        self.ge.putLabel(labelReturn)
        self.ge.addEndFuncion()
        self.ge.inNativas = False

    def Lower(self):
        if self.ge.diccionarioNativas["lower"]:
            return
        self.ge.diccionarioNativas["lower"]=True
        self.ge.inNativas=True
        self.ge.addInicioFuncion("lower")

        index = self.ge.addTemporal()
        self.ge.addExpresion('H','2','-',index)
        self.ge.getHeap(index,index)
        self.ge.addExpresion(index,'1','-',index)

        labelCiclo = self.ge.newLabel()
        labelAux = self.ge.newLabel()
        labelUpper = self.ge.newLabel()
        labelReturn = self.ge.newLabel()
        self.ge.addGoto(labelCiclo)
        self.ge.putLabel(labelCiclo)

        self.ge.addExpresion(index,'1','+',index)
        palabra = self.ge.addTemporal()
        self.ge.getHeap(palabra,index)
        self.ge.addIf(palabra,'-1','==',labelReturn)
        self.ge.addIf(palabra,'91','<',labelAux)
        self.ge.addGoto(labelCiclo)

        self.ge.putLabel(labelAux)
        self.ge.addIf(palabra,'64','>',labelUpper)
        self.ge.addGoto(labelCiclo)

        self.ge.putLabel(labelUpper)
        self.ge.addExpresion(palabra,'32','+',palabra)
        self.ge.setHeap(index,palabra)
        self.ge.addGoto(labelCiclo)

        self.ge.putLabel(labelReturn)
        self.ge.addEndFuncion()
        self.ge.inNativas = False

    def PrintArray(self):
        if self.ge.diccionarioNativas["printArray"]:
            return
        self.ge.diccionarioNativas["printArray"]=True
        self.ge.inNativas=True

        self.ge.addInicioFuncion("printArray")
        labelReturn=self.ge.newLabel()
        Pe = self.ge.addTemporal()      # a1
        posHeap = self.ge.addTemporal() #a2
        self.ge.addExpresion('H','','',Pe)  #a1=P
        self.ge.getHeap(posHeap,Pe)    #a2 = stack[int(a1)]
        tamano = self.ge.addTemporal()
        indice = self.ge.addTemporal()
        self.ge.getHeap(tamano,posHeap) #a3 = heap[int(a2)]
        self.ge.addExpresion('1','','',indice)
        ciclo = self.ge.newLabel()
        
        self.ge.putLabel(ciclo)
        self.ge.addExpresion(posHeap,'1','+',posHeap)
        obtenido=self.ge.addTemporal()
        self.ge.getHeap(obtenido,posHeap)
        self.ge.addIf(indice,tamano,'>',labelReturn)
        self.ge.addPrint("d",obtenido)
        self.ge.addPrint("c",45)
        self.ge.addExpresion(indice,'1','+',indice)
        self.ge.addGoto(ciclo)

        self.ge.putLabel(labelReturn)
        self.ge.addEndFuncion()
        self.ge.inNativas = False