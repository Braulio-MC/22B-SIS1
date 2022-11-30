import React from 'react';
import "./loginform.css"
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

    const navR = () => {
        navigate("/Registrar")
    }

    const recarga = () => {
        navigate("/")
    }

    const logout = () => {
        sessionStorage.clear();
        recarga();
    }

    return (
        <div className="tool-bar">
            <NavLink to='/' className="ContenedorLogo">
                <img className='logo' src={Logo}/>
            </NavLink>
            <div className="login-btn2" onClick={navC}>
                Carreras
            </div>
            <div className="login-btn2" onClick={navM}>
                Modulares
            </div>
            <div className="login-btn2" onClick={navS}>
                Servicio
            </div>
            {!sessionStorage.getItem('accessToken') 
             ?
             <>
                <div className="login-btn2" onClick={navL}>Autenticar</div> 
                <div className="login-btn2" onClick={navR}>Registrar</div>
             </> 
             :
             <>
                <div className='login-btn3' onClick={logout}>Salir</div>
             </>
            }
        </div>
    );
}

export default Menu;