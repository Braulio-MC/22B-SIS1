import React, {Fragment, useState } from "react";
import "./loginform.css"
import { NavLink } from 'react-router-dom';
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

    const [datos,setDatos] = useState({
        student_code:'',
        student_password:''
    })

    const handleInputChange = (event) => {
        // console.log(event.target.name)
        // console.log(event.target.value)
        setDatos({
            ...datos,
            [event.target.name] : event.target.value
        })
    }
    const enviarDatos = (event) => {
        event.preventDefault()
        console.log(datos.student_code + ' ' + datos.student_password)
    }

    console.log(datos.student_code + ' ' + datos.student_password)

        return(
        <Fragment>
<form onSubmit={enviarDatos}>
   <div className="covertest">
            <div className="relleno">   
        </div>
        <div className="cover">
            <h1>Login</h1>
                <input type="text" placeholder="student_code" onChange={handleInputChange} name="student_code"/>
                <input type="password" placeholder="student_password" onChange={handleInputChange} name="student_password"/>
            
            
            <div type="submit" className="btn btn-primary">
                Login
            </div>
            <div>¿Eres nuevo en WikiMaterias?</div>
            <div  className="login-btn2">
            <NavLink to='/Registrar' >
                Registrate
            </NavLink>
                </div>
        </div>
        <div className="relleno">   
        </div>
    </div>
</form>
    <ul>
                <li>{datos.student_code}</li>
                <li>{datos.student_password}</li>
            </ul>
    </Fragment>
    )
}

export default LoginForm