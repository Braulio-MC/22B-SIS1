import React, { useState } from 'react';
import "./loginform.css"
import ToolBar from "./ToolBar";
import Sidebar from "./Sidebar";
import Backdrop from './Backdrop';
import MenuFillIcon from 'remixicon-react/MenuFillIcon';
import {button} from 'react';
import carreras from './carreras';
import { useNavigate } from 'react-router-dom';
import { NavLink } from 'react-router-dom';


const Menu = () => {

    const Saludar = () =>{
        alert("Aún no se redireccionar")
    }

    return(
        
        <div className="tool-bar">
            <div className="burger">
                <i><MenuFillIcon/></i>
            </div>

            <NavLink to='/MainMenu' className="login-btn2">
                Menú
            </NavLink>
            <NavLink to='/carreras' className="login-btn2">
                Carreras
            </NavLink>
            <NavLink to='/Servicios' className="login-btn2">
                Servicios
            </NavLink>
            <NavLink to='/Login' className="login-btn2">
                Login
            </NavLink>
        
    </div>
    )
}

export default Menu