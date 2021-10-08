import React  from "react";

export class TablaErrores extends React.Component{

  state={
    error:[]
  }

  componentDidMount = () => {
    //console.log(this.props.listaErrores)
    var aux=[]
    var i=1
    this.props.listaErrores.forEach(element => {
      element["num"] = i
      i++
      aux.push(element)
    });
    this.setState({error:aux})
    if (aux.length===0){
      alert('lista errores vacia')
    }
  }

    render(){
        return(
            <div className="resultados">
          <table className="table table-striped table-hover table-light">
          <thead>
            <tr>
            <th scope="col">No.</th>
              <th scope="col">Fila</th>
              <th scope="col">Columna</th>
              <th scope="col">fecha</th>
              <th scope="col">Descripcion</th>
            </tr>
          </thead>
          <tbody style={{textAlign:'left'}}>
            {this.state.error.map(
              element => <tr key={element.num}>
                          <td>{element.num}</td>                                        
                          <td>{element.lin}</td>                                        
                          <td>{element.col}</td>                          
                          <td>{element.fecha}</td>                          
                          <td>{element.desc}</td>                          
                        </tr>
            )}
          </tbody>
          </table>
        </div> 
        );
    }
}