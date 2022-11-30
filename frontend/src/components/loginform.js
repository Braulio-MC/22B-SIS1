import React, { useState } from "react";
import "./loginform.css"
import { NavLink } from 'react-router-dom';
import "./Body.css"
import { useNavigate } from "react-router-dom";

/*
TENGO QUE PASAR UN JSON CON:
student_code
student_password

//////////////////////////////

CUENTA NUEVA:
    student_code
    student_name
    student_degree_code
    student_password
///////////////////////////////

*/

const LoginForm = () => {
    const navigate = useNavigate();
    const [token, setToken] = useState("");
    const [estudianteActual, setEstudianteActual] = useState({
        student_code: "",
        student_name: "",
        degree_code: "",
        modular_code: "",
        degree_name: "",
        creation_date: "",
        type: "",
    });
    const [datos, setDatos] = useState({
        student_code: '',
        student_password: ''
    });
    
    const handleInputChange = (event) => {
        setDatos({
            ...datos,
            [event.target.name] : event.target.value
        });
    }

    const fetchToken = async () => {
        try {
            let url = `http://192.9.147.109/login`;
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
            let url = `http://192.9.147.109/student/user-info`;
            let headers = {
                "X-Access-Token": sessionStorage.getItem('accessToken')
            };
            let response = await fetch(url, {
                headers: headers,
            });
            let data = await response.json();
            setEstudianteActual(data);
            if ("student_code" in data) {
                sessionStorage.setItem("student_code", data["student_code"]);
                sessionStorage.setItem("student_name", data["student_name"]);
                sessionStorage.setItem("degree_code", data["degree_code"]);
                sessionStorage.setItem("modular_code", data["modular_code"]);
                sessionStorage.setItem("degree_name", data["degree_name"]);
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
        if (datos.student_code.match('^[0-9]{9}$'))
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
        navigate("/")
    }

    return (
        <div className="Fondo">
            <form onSubmit={enviarDatos}>
                <div className="body">
                    <div className="relleno"></div>
                    <div className="cover">
                        <h1>Inicio de sesión</h1>
                        <input type="text" placeholder="Código de estudiante" onChange={handleInputChange} name="student_code"/>
                        <input type="password" placeholder="Contraseña" onChange={handleInputChange} name="student_password"/>
                        <input type="submit" className="btn btn-primary" value="Iniciar sesión" />
                        <div>¿Eres nuevo en WikiMaterias?</div>
                        <div className="login-btn2">
                            <NavLink to='/Registrar'>
                                Registrate
                            </NavLink>
                        </div>
                    </div>
                    <div className="relleno"></div>
                </div>
            </form>
        </div>
    );
}

export default LoginForm;