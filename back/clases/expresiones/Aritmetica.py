from enum import Enum
import re
from clases.abstract.Expresion import *
from clases.abstract.Return import *
from clases.enviroment.Generator import Generator
class OperacionesAritmeticas(Enum):
    SUMA = 0
    RESTA = 1
    MULTI = 2
    DIV = 3
    MODULO=4
    POTENCIA=5

class OperacionAritmetica(Expresion):
    def __init__(self,izquierdo,derecho,tipo, line, column):
        Expresion.__init__(self,line, column)
        self.izquierdo=izquierdo
        self.derecho=derecho
        self.tipo=tipo

    def compilar(self, enviroment):
        # obteniendo generador
        aux = Generator()
        generador = aux.getInstance()
        # compilando valores
        try:
            izq=self.izquierdo.compilar(enviroment)
            der=self.derecho.compilar(enviroment)
            ope = ""
            res = Return()

            if(self.tipo==OperacionesAritmeticas.SUMA):
                res = self.sumaRestaMult(izq,der)
                ope="+"
            elif (self.tipo==OperacionesAritmeticas.RESTA):
                res = self.sumaRestaMult(izq,der)
                ope="-"
            elif (self.tipo==OperacionesAritmeticas.MULTI):
                res = self.multiplicacion(izq,der)
                if res.tipo==Type.STRING:
                    return res
                ope="*"
            elif (self.tipo==OperacionesAritmeticas.DIV):
                res = self.division(izq,der)
                if res==None: return Return()
                ope="/"
                aux = Generator()
                generador = aux.getInstance()
                temp = generador.addTemporal()
                divisor = generador.addTemporal()
                generador.addExpresion(der.valor,'','',divisor)
                generador.funPrintMathError()

                lblError = generador.newLabel()
                lblContinue = generador.newLabel()
                generador.addIf(divisor,'0','!=',lblError)
                generador.callFun("mathError")
                generador.addPrint("c",10)
                generador.addExpresion(0,'','',temp)
                generador.addGoto(lblContinue)
                generador.putLabel(lblError)
                generador.addExpresion(izq.valor,divisor,ope,temp)
                generador.putLabel(lblContinue)
                res.valor = temp
                return res
            elif (self.tipo==OperacionesAritmeticas.MODULO):
                res = self.modulo(izq,der)
                if res == None: return Return()
                temp = generador.addTemporal()
                generador.activarModulo(izq.valor,der.valor,temp)
                res.valor = temp
                return res
            elif self.tipo==OperacionesAritmeticas.POTENCIA:
                res = self.potencia(izq,der,enviroment)
                if res == None: return Return()
                if res.tipo==Type.STRING: return res
                generador.funPotencia()
                return res
            if res ==None:
                generador.funPrintMathError()
                generador.callFun("mathError")
                generador.addPrint("c",10)
                return Return(0,Type.INT,False)
            temp = generador.addTemporal()
            generador.addExpresion(izq.valor,der.valor,ope,temp)
            res.valor = temp
            return res
        except:
            print("error inesperado en la operacion binaria")
    
    def sumaRestaMult(self,izq,der):
        if not(izq.tipo==Type.INT or izq.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        if not(der.tipo==Type.INT or der.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        
        if (izq.tipo==Type.FLOAT or der.tipo==Type.FLOAT):
            return Return(0,Type.FLOAT,True)
        return Return(0,Type.INT,True)
    
    def multiplicacion(self,izq,der):
        if not(izq.tipo==Type.INT or izq.tipo==Type.FLOAT or izq.tipo==Type.STRING):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        if not(der.tipo==Type.INT or der.tipo==Type.FLOAT or der.tipo==Type.STRING):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        if (izq.tipo==Type.STRING or der.tipo==Type.STRING):
            #resultado = str(izq.valor)+str(der.valor)
            aux = Generator()
            generador = aux.getInstance()
            generador.funConcatenarString()
            # demas codigo
            generador.addComent("aritmetica concatenacion")
            generador.setHeap('H',izq.valor)
            generador.nextHeap()
            generador.setHeap('H',der.valor)
            generador.nextHeap()
            generador.setHeap('H','-1')
            generador.nextHeap()
            generador.callFun("concatenarString")
            #generador.addExpresion(izq.valor,'','','H')
            generador.addComent("fin concatenacion")
            return Return(izq.valor,Type.STRING,True)
        if (izq.tipo==Type.FLOAT or der.tipo==Type.FLOAT):
            return Return(0,Type.FLOAT,True)
        return Return(0,Type.INT,True)
    
    def division(self,izq,der):
        if not(izq.tipo==Type.INT or izq.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        if not(der.tipo==Type.INT or der.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 

        if (izq.tipo==Type.FLOAT or der.tipo==Type.FLOAT):
            return Return(0,Type.FLOAT,True)
        else:
            if izq.esTemp or der.esTemp:
                return Return(0,Type.FLOAT,True)
            v = izq.valor/der.valor
            formato = re.compile(r'^\-?[1-9][0-9]*$')
            if re.match(formato,str(v)):
                v = int(v)
                return Return(0,Type.INT,True)
            else:
                return Return(0,Type.FLOAT,True)

    def modulo(self,izq,der):
        if not(izq.tipo==Type.INT or izq.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        if not(der.tipo==Type.INT or der.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        
        if (izq.tipo==Type.FLOAT or der.tipo==Type.FLOAT):
            return Return(0,Type.FLOAT,True)
        return Return(0,Type.INT,True)
    
    def potencia(self,izq,der,enviroment):
        if (izq.tipo==Type.STRING and der.tipo==Type.INT):
            return self.potenciaString(izq,der)
        if not(izq.tipo==Type.INT or izq.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        if not(der.tipo==Type.INT or der.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        
        aux = Generator()
        genrador:Generator = aux.getInstance()
        # ingresando valores a stack
        genrador.addExpresion('P',enviroment.size,'+','P')    #   p=p+1
        genrador.setStack('P',izq.valor)        #   stack[int(P)]=izq;
        genrador.addExpresion('P',1,'+','P')    #   p=p+1
        genrador.setStack('P',der.valor)        #   stack[int(P)]=der;
        genrador.addExpresion('P',1,'+','P')    #   p=p+1
        genrador.callFun("potencia")


        # recuperamos el dato y mostramos
        resultado = genrador.addTemporal()  # t
        genrador.getStack(resultado,'P')    #t=stack(P)
        genrador.addExpresion('P',enviroment.size,'-','P')
        res = Return()
        if (izq.tipo==Type.FLOAT or der.tipo==Type.FLOAT):
            res= Return(0,Type.FLOAT,True)
        else:
            res= Return(0,Type.INT,True)

        res.valor = resultado
        return res

    def potenciaString(self,izq,der):
        aux = Generator()
        generador = aux.getInstance()
        generador.funcPotenciaString()
        generador.addComent("Inicio Potencia String")
        generador.addComent("aritmetica potencia")
        generador.setHeap('H',izq.valor)
        generador.nextHeap()
        generador.setHeap('H',der.valor)
        generador.nextHeap()
        generador.setHeap('H','-1')
        generador.nextHeap()
        generador.callFun("potenciaString")
        #generador.getHeap('H','H')
        generador.addComent("Fin potencia String")

        return Return(0,Type.STRING,True)