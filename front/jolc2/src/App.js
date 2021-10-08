import './App.css';
import {Home} from './components/home/home'
import { Compiler } from './components/compiler/compiler';
import { Resports } from './components/reports/reportes';
import {Redirect, Route,Router,Switch} from 'react-router-dom'
import history from './history'

function App() {
  return (
    <div className="App" >
      <Router history={history}>
        <Switch>
          <Route exact path="/">
            <Home/>
          </Route>
          <Route exact path="/compiler">
            <Compiler/>
          </Route>
          <Route exact path="/reports:result">
            <Resports className="cuerpo"/>
          </Route>
          <Route path="/404" component={Home} />
          <Redirect to="/"/>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
