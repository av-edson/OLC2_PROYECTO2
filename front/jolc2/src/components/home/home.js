import React from "react";
import '../../App.css'
import { NavBar } from "../nav/navbar";
import foto from './yo2.jpg'

export class Home extends React.Component{

    render () {
        return(
            <div>
                <NavBar/>
                <div className="datos">
                    <div className="card" style={{width: "18rem"}}>
                      <img src={foto} alt="" className="card-img-top"></img>
                      <div className="card-body">
                        <h5 className="card-title">Edson Avila</h5>
                        <p className="card-text">201902302
                            Compiladores 2 Seccion C
                            Proyecto 2
                        </p>
                      </div>
                    </div>
                </div>
                <footer style={{backgroundColor:"aliceblue"}}>
                  <p>Todos los derechos reservador @Edson Avila
                    <a href="https://github.com/av-edson">av-edson</a>
                  </p>
                </footer>
            </div>
        );
    }
}