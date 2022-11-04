/**
 * 
 * AQUI SOLAMENTE ESTAMOS HACIENDO FUNCION DE CERRAR EL SIDEBAR
 * 
 * 
 */
import React from "react";

const Backdrop = ({sidebar, closeSidebar}) =>{
    return(
        <div className={sidebar?"backdrop  backdrop--open":"backdrop"} onClick={closeSidebar}></div>
    )
}
export default Backdrop 