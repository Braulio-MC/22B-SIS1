import React, { useState } from 'react';
import "./loginform.css"
import ToolBar from "./ToolBar";
import Sidebar from "./Sidebar";
import Backdrop from './Backdrop';
import MenuFillIcon from 'remixicon-react/MenuFillIcon';
import {button} from 'react';
import carreras from './carreras';
import { useNavigate } from 'react-router-dom';


const Menu = () => {

    const Saludar = () =>{
        alert("Aún no se redireccionar")
    }



    return(
        
        <div className="tool-bar">
            <div className="burger">
                <i><MenuFillIcon/></i>
            </div>

            <div className="login-btn" onClick={Saludar}>
                Menú
            </div>
            <div className="login-btn" onClick={Saludar}>
                Carreras
            </div>
            <div className="login-btn" onClick={Saludar}>
                Servicio
            </div>
            <div className="login-btn" onClick={Saludar}>
                Login
            </div>
            <a href='/'> Menú</a>
            <a href='/carreras'> Carreras</a>
            <a href='/login'>Login</a>
        
    </div>
    )
}

export default Menu