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
            der=self.derecho.compilar(enviroment)
            izq=self.izquierdo.compilar(enviroment)
            ope = ""
            res = Return()

            if(self.tipo==OperacionesAritmeticas.SUMA):
                res = self.sumaRestaMult(izq,der)
                if res == None: return Return()
                ope="+"
            elif (self.tipo==OperacionesAritmeticas.RESTA):
                res = self.sumaRestaMult(izq,der)
                if res == None: return Return()
                ope="-"
            elif (self.tipo==OperacionesAritmeticas.MULTI):
                res = self.sumaRestaMult(izq,der)
                if res == None: return Return()
                ope="*"
            elif (self.tipo==OperacionesAritmeticas.DIV):
                res = self.division(izq,der)
                if res == None: return Return()
                ope="/"
            elif (self.tipo==OperacionesAritmeticas.MODULO):
                res = self.modulo(izq,der)
                if res == None: return Return()
                temp = generador.addTemporal()
                generador.activarModulo(izq.valor,der.valor,temp)
                res.valor = temp
                return res
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
    def division(self,izq,der):
        if not(izq.tipo==Type.INT or izq.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        if not(der.tipo==Type.INT or der.tipo==Type.FLOAT):
            print("Tipo de Dato no admitido en operacion aritmetica")
            return 
        if int(der.valor)==0:
            print("Division por 0 no admitida")
            aux = Generator()
            generador = aux.getInstance()
            generador.funPrintMathError()
            generador.callFun("mathError")
            generador.addPrint("c",10)
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

