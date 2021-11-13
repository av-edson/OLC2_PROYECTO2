import flask
from flask import request
from flask_cors import CORS
from controller import analizarEntrada,Regreso

app = flask.Flask(__name__)
CORS(app)
#app.config["DEBUG"] = True
anterior=None
 
@app.route('/', methods=['GET'])
def home():
    response = flask.jsonify({"mensaje":"estamos funcionando"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    
@app.route('/', methods=['POST'])
def compilar():
    try:
        content = request.get_json()
        ret:Regreso = analizarEntrada(content['code'])
        global anterior
        anterior=ret
        response = flask.jsonify({"value":ret.compilacion,"consola":ret.consola,"errores":ret.errores,"tabla":ret.tabla})

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except:
        ret:Regreso = Regreso(False,"Un error al compilar Ocurrio","","")
        response = flask.jsonify({"value":ret.compilacion,"consola":ret.consola,"errores":ret.errores,"tabla":ret.tabla})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/GetLast', methods=['GET'])
def obtener():
    global anterior
    if anterior == None:
        ret:Regreso = Regreso(False,"No se ha compilado ninguna entrada para reporte","","")
        response = flask.jsonify({"value":ret.compilacion,"consola":ret.consola,"errores":ret.errores,"tabla":ret.tabla})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = flask.jsonify({"value":anterior.compilacion,"consola":anterior.consola,"errores":anterior.errores,"tabla":anterior.tabla})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
if __name__ == '__main__':
    app.run()