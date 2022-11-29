import React from 'react';
import "./loginform.css"
import MenuFillIcon from 'remixicon-react/MenuFillIcon';
import { NavLink, useNavigate } from 'react-router-dom';

import Logo from "./imagenes/LogoWM.png"


const Menu = () => {

    const navigate = useNavigate();

    const navC = () => {
        navigate("/carreras")
    }
    const navM = () => {
        navigate("/modulares")
    }
    const navS = () => {
        navigate("/servicios")
    }
    const navL = () => {
        navigate("/login")
    }

    return(
        <div className="tool-bar">
            <NavLink to='/inicio' className="ContenedorLogo">
                <img className='logo' src={Logo}/>
            </NavLink>
            <div className="login-btn2" onClick={navC}>
                Carreras
            </div>
            <div className="login-btn2" onClick={navM}>
                Modulares
            </div>
            <div className="login-btn2" onClick={navS}>
                Servicios
            </div>
            <div className="login-btn2" onClick={navL}>
                Login
            </div>
        </div>
    );
}

export default Menu;