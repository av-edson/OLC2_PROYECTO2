import React from "react";
import { NavBar } from "../nav/navbar";
import { UnControlled as CodeMirror } from 'react-codemirror2';
import 'codemirror/theme/material.css';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/lib/codemirror.css';
import './stilo.css';
import history from "../../history";

export class Compiler extends React.Component{
    state={
        value:'',
        estado:true,
        code:''
    }

    onChange = (editor, data, value) => {
      this.setState({
        code:'',
        console:'',
        estado:true,
      });
    };
    render(){
        return(
            <div className='todo'>
                <NavBar/>
                <h2 style={{backgroundColor:"#27AE60"}}>JOLC Compiler</h2>
                <div className="editor">
                    <h3>Entrada de Codigo</h3>
                  <CodeMirror
                    value={this.state.code}
                    options={{
                      mode: 'javascript',
                      theme: 'material',
                      lineNumbers: true
                    }}
                    onChange={(editor, data, value) => {
                      this.setState({code:value})
                    }}
                  />
                </div>
                <div className="editor">
                <h3>Salida de Codigo</h3>
                  <CodeMirror
                    value={this.state.code}
                    options={{
                      mode: 'javascript',
                      theme: 'material',
                      lineNumbers: true
                    }}
                    onChange={(editor, data, value) => {
                      this.setState({code:value})
                    }}
                  />
                </div>
                <div className="d-grid gap-1">
                      <button className="btn btn-outline-success btn-lg " type="button" onClick={()=>this.verReportes()}>Ver Reportes
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" className="bi bi-window-dock" viewBox="0 0 16 16">
                          <path fillRule="evenodd" d="M15 5H1v8a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V5zm0-1H1V3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v1zm1-1a2 2 0 0 0-2-2H2a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V3z"/>
                          <path d="M3 11.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm4 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1zm4 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1z"/>
                        </svg>
                      </button>
                    </div>
                    <br/>
                  {this.state.estado?
                        <div className="btn-group btn-group-lg" role="group" aria-label="Basic example">
                          <button type="button" className="btn btn-outline-secondary">Compilar</button>
                          <button type="button" className="btn btn-outline-secondary">Optimizar Por Mirilla</button>
                          <button type="button" className="btn btn-outline-secondary">Optimizar Port Bloques</button>
                        </div>:
                    <div className="d-grid gap-3" id="cargando">
                      <div className="spinner-border" role="status">
                        <span className="visually-hidden">Loading...</span>
                      </div>
                    </div>
                }
                <br></br>
            </div>
        );
    }

    compilar(){
      alert('compilando joto')
    }
    
    verReportes(){
        var res = { "username": 2 }
        history.push(`/reports${res}`)
    }
}