import React, { useState } from "react";
import "./carreras.css"
import "bootstrap/dist/css/bootstrap.min.css";
import "styled-components";
import { useNavigate } from "react-router-dom";
import StarRating from "./StarRating";
import ChangeRating from "./ChangeRating";
import "./Body.css";


const Servicios = () => {
    const navigate = useNavigate();
    const [degree, setDegree] = useState([]);

    const [avgRating, setAvgRating] = useState(0);

  const handleRating = (input) => {
    setAvgRating(input);
  };

    return (
        <div className="Fondo">
            <div className="relleno"></div>
            <div className="Body">
                <h1>Servicio Social</h1>
                <div className="Parrafo">
                    <div>
                        El Servicio Social es la actividad formativa y de aplicación de conocimientos que de manera temporal y obligatoria realizan los alumnos o pasantes de la Universidad en beneficio de la sociedad,
                        del Estado y de la propia Universidad.
                    </div>
    
                    <div>    
                        De acuerdo con la visión de la Universidad de Guadalajara, el servicio social debe atender dos ámbitos:
                        <div className="linea">I. El Académico que le permite al estudiante llevar a la práctica los conocimientos que se han adquirido al tiempo que complementa su formación teórico-profesional.</div>
                        <div>II. El Social mediante el cual, el alumno puede acercarse a las comunidades de mayor rezago social, apoyar con sus conocimientos profesionales, sensibilizándose y obteniendo una serie de valores humanos y sociales que consolidan su formación integral y de excelencia.</div>
                        <div>La prestación del servicio social es un requisito indispensable para la titulación de los programas educativos de licenciatura del Sistema de Universidad Virtual.</div>
                    </div>
                </div>
                <div className="relleno"></div>
            <div className="App">
            <ChangeRating rating={avgRating} handleRating={handleRating} />
             <br />
             <br />
             <StarRating stars={avgRating} />
            </div>
            </div>
            
        </div>    
    );
}

export default Servicios