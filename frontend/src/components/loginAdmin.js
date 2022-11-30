import React, { useState } from "react";
import "./loginform.css"
import "./Body.css"
import { useNavigate } from "react-router-dom";


const LoginAdminForm = () => {
    const navigate = useNavigate();
    const [token, setToken] = useState("");
    const [adminActual, setAdminActual] = useState({
        admin_code: "",
        admin_name: "",
        admin_status: "",
        creation_date: "",
        type: ""
    });
    const [datos, setDatos] = useState({
        admin_code: '',
        admin_password: ''
    });
    
    const handleInputChange = (event) => {
        setDatos({
            ...datos,
            [event.target.name] : event.target.value
        });
    }

    const fetchToken = async () => {
        try {
            let url = `http://192.9.147.109/admin/login`;
            let headers = {
                "Content-Type": "application/json",
            };
            let response = await fetch(url, {
                method: 'POST',
                headers: headers,
                body: JSON.stringify(datos)
            });
            let token = await response.json();
            setToken(token);
            if ("token" in token)
                sessionStorage.setItem("accessToken", token["token"]);
            else
                alert("Credenciales invalidas")
        } catch (error) {
            alert("Ha ocurrido un error al iniciar sesión");
        }
    };

    const fetchUserInfo = async () => {
        try {
            let url = `http://192.9.147.109/admin/user-info`;
            let headers = {
                "X-Access-Token": sessionStorage.getItem('accessToken')
            };
            let response = await fetch(url, {
                headers: headers,
            });
            let data = await response.json();
            console.log(data);
            setAdminActual(data);
            if ("admin_code" in data) {
                sessionStorage.setItem("admin_code", data["admin_code"]);
                sessionStorage.setItem("admin_name", data["admin_name"]);
                sessionStorage.setItem("admin_status", data["admin_status"]);
                sessionStorage.setItem("creation_date", data["creation_date"]);
                sessionStorage.setItem("type", data["type"]);
            }
        } catch (error) {
            alert("Ha ocurrido un error al iniciar sesión");
        }
    };
    
    const setSesion = async () => {
        try {
            await fetchToken();
            await fetchUserInfo();
        } catch (error) {
            alert("Ha ocurrido un error al iniciar sesión");
        }
    }

    const validaCodigo = () => {
        if (datos.admin_code.match('^[0-9a-zA-Z]{8}$'))
            return true;
        return false;
    }

    const enviarDatos = (event) => {
        event.preventDefault();
        if (validaCodigo()){
            setSesion();
            navR();
        }
        else
            alert('Algun dato es incorrecto');
        
    }

    const navR = () => {
        navigate("/");
        setTimeout(() => {
            window.location.reload();
        }, 500);
    }

    return (
        <div className="Fondo">
            <form onSubmit={enviarDatos}>
                <div className="body">
                    <div className="relleno"></div>
                    <div className="cover">
                        <h1>Inicio de sesión</h1>
                        <input type="text" placeholder="Código de administrador" onChange={handleInputChange} name="admin_code"/>
                        <input type="password" placeholder="Contraseña" onChange={handleInputChange} name="admin_password"/>
                        <input type="submit" className="btn btn-primary" value="Iniciar sesión" />
                    </div>
                    <div className="relleno"></div>
                </div>
            </form>
        </div>
    );
}

export default LoginAdminForm;