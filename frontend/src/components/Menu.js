import React from 'react';
import "./loginform.css"
import MenuFillIcon from 'remixicon-react/MenuFillIcon';
import { NavLink } from 'react-router-dom';


const Menu = () => {
    return(
        <div className="tool-bar">
            <div className="burger">
                <i><MenuFillIcon/></i>
            </div>
            <NavLink to='/inicio' className="login-btn2">
                Menú
            </NavLink>
            <NavLink to='/carreras' className="login-btn2">
                Carreras
            </NavLink>
            <NavLink to='/modulares' className="login-btn2">
                Modulares
            </NavLink>
            <NavLink to='/servicio' className="login-btn2">
                Servicios
            </NavLink>
            <NavLink to='/login' className="login-btn2">
                Login
            </NavLink>
        </div>
    );
}

export default Menu;