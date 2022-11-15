/*
ESTE JS ES EL MENU PRINCIPAL DE NUESTRA APLICACION,
AQUI MOSTRAREMOS LA INFORMACION DE MATERIAS, MODULAR Y SERVICIO
*/
import React from 'react'
import MenuFillIcon from 'remixicon-react/MenuFillIcon';
const ToolBar = ({openSidebar}) => {
    return(
   <div>
        <div className="tool-bar">
            <div className="burger" onClick={openSidebar}>
                <i><MenuFillIcon/></i>
            </div>
            <div className="title"> Menú</div>
        </div>
            

    </div>
    )
}
export default ToolBar