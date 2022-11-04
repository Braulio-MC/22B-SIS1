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
            <div className="coverMenu">
                <div className="coverHead">
                    AQUI IRA EL TITULO QUE OBTENDRA DE TODOS LADOS, IGUALAREMOS ESTE ID (VARIABLE GLOBAL)
                </div>
                <div className="coverMenus">
                    AQUI PONDREMOS TODA LA DESCRIPCION DE TODOS LOS DATOS, IGUALREMOS ESTE ID (VARIABLE GLOBAL A TODOS LOS DATOS)
                </div>
                <div className="relleno"></div>
            </div>

    </div>
    )
}
export default ToolBar