import React from "react";
import '../../App.css'
import { NavBar } from "../nav/navbar";

export class Home extends React.Component{

    render () {
        return(
            <div>
                <NavBar/>
                <div className="datos">
                    <div className="card" style={{width: "18rem"}}>
                      <img src="https://scontent-mia3-1.xx.fbcdn.net/v/t1.6435-9/215278960_4096888383721957_5057494979382707356_n.jpg?_nc_cat=100&ccb=1-5&_nc_sid=09cbfe&_nc_ohc=v0sd6457TzIAX_L_loz&_nc_ht=scontent-mia3-1.xx&oh=b84ab5c374b384e21bfd9816d0d85e3d&oe=618624BF" alt="" className="card-img-top"></img>
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