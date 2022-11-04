/** 
 * AQUI ESTAMOS VISUALIZANDO EL SLIDEBAR, AQUI MOSTRAREMOS 

*/
import React from "react";
import HomeIcon from 'remixicon-react/Home2FillIcon'
import BookIcon from 'remixicon-react/Book2FillIcon'
import MO from 'remixicon-react/BookOpenLineIcon'
import ME from 'remixicon-react/Book3LineIcon'
import Mod from 'remixicon-react/MediumFillIcon'
import Ss from 'remixicon-react/GlobeFillIcon'
import Lo from 'remixicon-react/LoginCircleLineIcon'

const Sidebar = ({sidebar}) => {


    return(
        <div className={sidebar?"sidebar sidebar--open":"sidebar"}>
                <li><HomeIcon/>Home</li>
                <li><BookIcon/>Carreras</li>
                <li><MO/>Materias Optativas</li>
                <li><ME/>Materias Especializantes</li>
                <li><Mod/>Modular</li>
                <li><Ss/>Servicio social</li>
                <li><Lo/>Login</li>
        </div>
    )
}

export default Sidebar