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

    const nav = (props) => {
        navigate("/servicio", { state: {rowData: props} })
    }

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
                    Es una actividad formativa y de aplicación de conocimientos que de manera temporal
                    y obligatoria realizan los alumnos o pasantes de la universidad de Guadalajara al beneficio
                    de la sociedad, del estado y de la propia Universidad.
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