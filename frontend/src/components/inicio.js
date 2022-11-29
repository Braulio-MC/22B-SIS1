import React, { useState } from "react";
import "./carreras.css"
import "bootstrap/dist/css/bootstrap.min.css";
import "styled-components";
import { useNavigate } from "react-router-dom";
//import { Image} from "react-native";


const Inicio = () => {
    const navigate = useNavigate();
    const [degree, setDegree] = useState([]);

    const nav = (props) => {
        navigate("/Inicio", { state: {rowData: props} })
    }

    return (
        <div >
            <div className="relleno"></div>
            <div>
                <h1>Wiki Materias</h1>
                <image  style={{ width: 100, height: 100, marginBottom: 15 }} source={require('./imagenes/LogoWM.png')}></image>
                <div className="Parrafo">
                    Wiki materias nace de la necesidad de poder tener una funte confiable de información
                    que por medio de consultar tu carrera y alguna materia, la aplicación te brindará un breve resumen
                    sobre de que trata la materia, con el objetivo de guiarte y poderte brindar conocimiento de la materia.

                    Asi mismo, podrás consultar información acerca de materias optativas, especializantes, proyectos modulares y servicio social.
                </div>
            </div>
            <div className="relleno"></div>
        </div>    
    );
}

export default Inicio;