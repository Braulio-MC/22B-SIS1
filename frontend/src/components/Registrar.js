import React, {Fragment, useState, useEffect } from "react";
import "./loginform.css"
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

const Registrar = () => {
    const navigate = useNavigate();
    const [codigoCarrera, setCodigoCarrera] = useState([])
    const [datos, setDatos] = useState({
        student_code:'',
        student_name:'',
        student_degree_code:'INNI',
        student_password:''
    })

    const [Codigo,SetDatos] = useState({
        student_degree_code:'INNI'
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

    const enviarDatos = (event) => {
        event.preventDefault()
        signinUser();
        navR();
    }

    const navR = () => {
        navigate("/login")
    }

    console.log(datos.student_code + ''+ datos.student_name + '' + datos.student_degree_code + ' ' + datos.student_password )

        return(

        <Fragment>
<form onSubmit={enviarDatos}>
   <div className="Fondo">
            <div className="relleno">   
        </div>
        <div className="cover">
            <h1>Registrar</h1>
                <input type="text" placeholder="student_code" onChange={handleInputChange} name="student_code"/>
                <input type="text" placeholder="student_name" onChange={handleInputChange} name="student_name"/>

                <input list="text" placeholder="student_degree_code" onChange={handleInputChange} name="student_degree_code" />
                <datalist id="Degree">
                   <option value={datos.student_degree_code}></option>
                </datalist>                   


                <input type="password" placeholder="student_password" onChange={handleInputChange} name="student_password"/>

            <input type="submit" className="btn btn-primary" value={"Registrar"}>
                
            </input>
        </div>
        <div className="relleno">   
        </div>
    </div>
</form>
    <ul>
                <li>{datos.student_name}</li>
                <li>{datos.student_code}</li>
                <li>{datos.student_password}</li>
                <li>{datos.student_degree_code}</li>
            </ul>
    </Fragment>
    )
}

export default Registrar;