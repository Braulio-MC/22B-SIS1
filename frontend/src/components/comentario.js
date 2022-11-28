import React from "react";

const Comentario = (props) => {
    
    return(
        <div className="ComentarioCaja">
            <div className="ComentarioUsuario">{props.usuario}</div>
            <div className="ComentarioRanking">{props.ranking}/5</div>
            <div className="ComentarioContenido">{props.comentario_contenido}</div>
            
        </div>
    )
}

export default Comentario