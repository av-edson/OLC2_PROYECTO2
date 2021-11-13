import React  from "react";

export class TablaSimbolos extends React.Component{
  state={
    simbolos:[]
  }

  componentDidMount = () => {
    //console.log(this.props.listaErrores)
    var aux=[]
    var i=1
    
    this.props.listaSimbolos.forEach(element => {
      element["num"] = i
      i++
      aux.push(element)
    });
    this.setState({simbolos:aux})
    if (aux.length===0){
      alert('lista simbolos vacia')
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
              <th scope="col">Ambito</th>
              <th scope="col">Nombre</th>
              <th scope="col">Tipo</th>
              <th scope="col">Valor</th>
            </tr>
          </thead>
          <tbody style={{textAlign:'left'}}>
            {this.state.simbolos.map(
              element =>
              <tr key={element.num}>
                <td >{element.num}</td>
                <td >{element.fila}</td>
                <td >{element.columna}</td>
                <td >{element.ambito}</td>
                <td >{element.nombre}</td>
                <td >{element.tipo}</td>
                <td >{element.valor}</td>
              </tr>
            )}
          </tbody>
          </table>
        </div> 
        );
    }
}