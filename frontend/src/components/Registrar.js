import React, {Fragment, useState } from "react";
import "./loginform.css"
import Combobox from "react-widgets/Combobox";

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

    const [CodigoCarrera,SetCodigoCarrera] = useState({
            
    })


    const [datos,setDatos] = useState({
        student_code:'',
        student_name:'',
        student_degree_code:'',
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
        console.log(datos.student_code + ''+ datos.student_name + '' + datos.student_degree_code + ' ' + datos.student_password )
    }

    console.log(datos.student_code + ''+ datos.student_name + '' + datos.student_degree_code + ' ' + datos.student_password )

        return(
        <Fragment>
<form onSubmit={enviarDatos}>
   <div className="covertest">
            <div className="relleno">   
        </div>
        <div className="cover">
            <h1>Registrar</h1>
                <input type="text" placeholder="student_code" onChange={handleInputChange} name="student_code"/>
                <input type="text" placeholder="student_name" onChange={handleInputChange} name="student_name"/>
                <Combobox data={CodigoCarrera}/>
                <input type="password" placeholder="student_password" onChange={handleInputChange} name="student_password"/>

            <div type="submit" className="btn btn-primary">
                Registrar
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

export default Registrar