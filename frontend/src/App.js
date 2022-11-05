import LoginForm from "./components/loginform"
import Menu from "./components/Menu"
import { Routes, Route } from "react-router-dom"

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
          <Route exact path="/login" element={<LoginForm />} />
          //? Aqui van los enlaces que quieras crear
          <Route path="*" element={''} />
        </Routes>                               
    </div>                                      
  );                                        
}

export default App;
