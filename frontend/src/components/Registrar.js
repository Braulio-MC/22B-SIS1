import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./loginform.css";
import "./Body.css";
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';


const Registrar = () => {
    const navigate = useNavigate();
    const [codigoCarrera, setCodigoCarrera] = useState([])
    const [datos, setDatos] = useState({
        student_code:'',
        student_name:'',
        student_degree_code:'',
        student_password:''
    })

    useEffect(() => {
        const fetchDegreeCodes = async () => {
            try {
                let url = `http://192.9.147.109/degree`;
                let response = await fetch(url);
                let data = await response.json();
                data = data.map((item) => {
                    return item['degree_code'];
                });
                setCodigoCarrera(data);
            } catch (error) {
                alert("Ha ocurrido un error al obtener los datos");
            }
        };
        fetchDegreeCodes();
    }, []);

    const signinUser = async () => {
        try {
            let url = `http://192.9.147.109/signin`;
            let headers = {
                "Content-Type": "application/json",
            };
            let response = await fetch(url, {
                method: 'POST', 
                headers: headers,
                body: JSON.stringify(datos)
            });
            let message = await response.json();
            alert(message['message']);
        } catch (error) {
            alert("Ha ocurrido un error al registrarse");
        }
    };

    const handleInputChange = (event) => {
        setDatos({
            ...datos,
            [event.target.name] : event.target.value,
        });
    }

    const navR = () => {
        navigate("/login")
    }

    const handleValueChange = (value) => {
        if (value) {
            setDatos({
                ...datos,
                student_degree_code: value
            });
        }
    }

    const validaDatos = () => {
        if (datos.student_code.match('^[0-9]{9}$') && datos.student_password < 25)
            return true;
        return false;
    }

    const enviarDatos = (event) => {
        event.preventDefault();
        if (validaDatos()) {
            signinUser();
            navR();
        } else {
            alert("Codigo invalido o contraseña mayor a 25 caracteres");
        }
    }

    return (
        <div className="Fondo">
            <form onSubmit={enviarDatos}>
                <div className="body">
                    <div className="relleno"></div>
                    <div className="cover">
                        <h1>Registrar</h1>
                        <input type="text" placeholder="Código de estudiante" onChange={handleInputChange} name="student_code"/>
                        <input type="text" placeholder="Nombre completo" onChange={handleInputChange} name="student_name"/>
                        <Autocomplete 
                            options={codigoCarrera}
                            style={{ width: 300 }}
                            renderInput={(params) => <TextField {...params} label="Código de carrera" />}
                            onChange={(e, v) => handleValueChange(v)}
                        />
                        <input type="password" placeholder="Contraseña" onChange={handleInputChange} name="student_password"/>
                        <input type="submit" className="btn btn-primary" value="Registrarse" />
                    </div>
                    <div className="relleno"></div>
                </div>
            </form>
        </div>
    );
}

export default Registrar;