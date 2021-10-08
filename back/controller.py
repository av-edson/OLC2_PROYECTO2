from analizadores.grammar import compilar
from clases.enviroment.Enviroment import Enviroment
from clases.enviroment.Generator import Generator

f = open('entrada.txt',encoding="UTF-8")
gl = Enviroment(None,"Global")
contenido = f.read()
ast = compilar(contenido)

try:
    genAux = Generator()
    genAux.limpiarTodo()
    generador = genAux.getInstance()

    for instruccion in ast:
        if instruccion != None:
            d=instruccion.compilar(gl)
        x = 4
    print(generador.getCodigo())
except:
    print("Error al ejecutar instrucciones")
