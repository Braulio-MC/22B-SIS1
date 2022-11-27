import LoginForm from "./components/loginform"
import Menu from "./components/Menu"
import Materias from "./components/materias"
import { Routes, Route } from "react-router-dom"
import Carreras from "./components/carreras";
import Materia from "./components/materia";
import Modulares from "./components/modulares";
import Modular from "./components/modular";

/**
 * NOTA
 * <Route path="*" element={''} />: 
 * Esta ruta es para enlaces que no existen
 * Cambia '' por el componente que quieres que se visualice cuando intenten acceder a ese enlace
 * Y esa ruta siempre es la ultima
 */

function App() {
  return (
    <div>
        <Menu/>
        <Routes>
          <Route exact path="/inicio" />
          <Route exact path="/login" element={<LoginForm />} />
          <Route exact path="/carreras" element={<Carreras />} />
          <Route exact path="/materias" element={<Materias />} />
          <Route exact path="/materia" element={<Materia />} />
          <Route exact path="/modulares" element={<Modulares />} />
          <Route exact path="/modular" element={<Modular />} />
          <Route path="*" element={''} />
        </Routes>                               
    </div>                                      
  );                                        
}

export default App;
