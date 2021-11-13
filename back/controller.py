from analizadores.grammar import compilar
from clases.nodo import Nodo
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator
from analizadores.lexer import errores,listaStructs


class Regreso:
    def __init__(self,comp,consola,er,table):
        self.compilacion=comp
        self.consola = consola
        self.errores =er
        self.tabla=table

def objToJson(obj):
    lista = []
    for er in obj:
        dic = {}
        dic["desc"]=er.desc
        dic["lin"]=er.lin
        dic["col"]=er.col
        dic["fecha"]=er.fecha
        lista.append(dic)
    return lista

def tablaToJson(obj):
    lista = []
    for var in obj:
        var = obj[var]
        dic = {}
        dic["ambito"]=var.ambito
        dic["tipo"]=var.tipo
        dic["valor"]=var.valor
        dic["nombre"]=var.nombre
        dic["fila"]=var.fila
        dic["columna"]=var.columna
        lista.append(dic)
    return lista


def analizarEntrada(contenido=None):
    try:
        #arbol:Nodo= parser2.parse(contenido)
        print(contenido)
        global errores,listaStructs
        errores.clear()
        listaStructs.clear()
        listaStructs.clear()
        ast = compilar(contenido)
        gl = Enviroment(None,"Global")
        try:
            genAux = Generator()
            genAux.limpiarTodo()
            generador = genAux.getInstance()

            for instruccion in ast:
                if instruccion != None:
                    d=instruccion.compilar(gl)
            #gl.addVariable_TablaSimbolos()
        except Exception as e:
            print("Error al Compilar instrucciones")
            return Regreso(False,str(e),"","","")
        a=errores+generador.listaErrores
        listJson = objToJson(errores)
        #tablaSimbolos = tablaToJson(gl.listaSimbolos)
        #abr = arbol.getGrafico()
        return Regreso(True,generador.getCodigo(),listJson,[])
    except Exception as e:
        return Regreso(False,str(e),"","","")

#f = open('entrada.txt',encoding="UTF-8")
#gl = Enviroment(None,"Global")
#contenido = f.read()
#ast = compilar(contenido)
#f.close()
#try:
#    genAux = Generator()
#    genAux.limpiarTodo()
#    generador = genAux.getInstance()
#
#    for instruccion in ast:
#        if instruccion != None:
#            d=instruccion.compilar(gl)
#        x = 4
#    #print(generador.getCodigo())
#    f = open('pruebas/salida.go','w',encoding="UTF-8")
#    f.write(generador.getCodigo())
#    f.close()
#    a= errores + generador.listaErrores
#    print(a)
#
#except:
#    print("Error al ejecutar instrucciones")


