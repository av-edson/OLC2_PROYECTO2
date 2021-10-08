import React from "react";
import { TablaErrores } from "./TablaErrores";
import { TablaSimbolos } from "./TablaSimbolos";
import './stilo.css'

export class Resports extends React.Component{


    state={
        dot:'',
        tabla:{},
        errores:{},
        mensajeRetorno:'Ninguna accion realizada'
    }

    componentDidMount = () => {
        this.getData();
      };
    
    getData = () => {
        this.setState({dot:'',
        tabla:[],
        errores:[],
        mensajeRetorno:'Ninguna accion realizada'})
        fetch('https://backapiolc2.herokuapp.com/GetLast',{
          method:'GET',
          headers: {"Content-Type":"application/json"}
        }).then(async response =>{
              //console.log('aca')
              const json = await response.json() 
              if (!json.value) {
                var mensaje = json.consola
               // console.log(mensaje)
                this.setState({mensajeRetorno:mensaje})
              }else{
                  var er = json.errores
                  var as = String(json.ast)
                  var sim = json.tabla
                  this.setState({mensajeRetorno:'Carga de Reportes exitosa',tabla:sim,dot:as,errores:er})
              }
              alert(this.state.mensajeRetorno)
            })
      };

    state={
        noReporte:0,
        tipoReporte:'Tabla de Errores'
    }

    render(){
        return(
            <div className="cuerpo2">
                <h2 style={{backgroundColor:"#27AE60"}}>Zona de Reportes</h2>
                <h3 style={{backgroundColor:"#27AE60"}}>Actual: {this.state.tipoReporte}</h3>
                <br></br>
                <div className="btn-group btn-group-lg" role="group" aria-label="Basic radio toggle button group">
                  <input type="button" className="btn-check" name="btnradio" id="btnradio1" autoComplete="off"
                  onClick={()=>this.cambio(1)}></input>
                  <label className="btn btn-outline-info" htmlFor="btnradio1">Tabla de Errores</label>

                  <input type="button" className="btn-check" name="btnradio" id="btnradio2" autoComplete="off"
                  onClick={()=>this.cambio(2)}></input>
                  <label className="btn btn-outline-info" htmlFor="btnradio2">Tabla de Simbolos</label>

                  <input type="button" className="btn-check" name="btnradio" id="btnradio3" autoComplete="off"
                  onClick={()=>this.cambio(3)}></input>
                  <label className="btn btn-outline-info" htmlFor="btnradio3">AST</label>
                </div> 
                
                <br></br>
                <br></br>
                <div className="tabla">
                {this.state.noReporte===1 &&
                    <TablaErrores listaErrores={this.state.errores}></TablaErrores>
                }   
                {this.state.noReporte=== 2 &&
                    <TablaSimbolos listaSimbolos={this.state.tabla}></TablaSimbolos>
                } 
                </div>
                      
            </div>
        );
    }

    cambio(a){
        this.setState({noReporte:a})
        switch (a) {
            case 1:
                this.setState({tipoReporte:'Tabla de Errores'})
                break;
            case 2:
                this.setState({tipoReporte:'Tabla de Simbolos'})
                break;
            case 3:
                this.setState({tipoReporte:'AST'})
                break;
            default:
                break;
        }
    }
}