import React, { useState, useEffect } from "react";
import "./carreras.css"
import "bootstrap/dist/css/bootstrap.min.css";
import "styled-components";
import MaterialTable from "material-table";
import { useNavigate } from "react-router-dom";
import "./Body.css"


const Carreras = () => {
    const navigate = useNavigate();
    const [degree, setDegree] = useState([]);
    const tipo = sessionStorage.getItem("type") == "admin" ? false : true; 

    const modificar = (props) => {
        console.log(props)
    } 

    const accionesUsuario = [
        {
            icon: 'M',
            tooltip: 'Visitar materias',
            onClick: (event, rowData) => navM(rowData)
        },
        {
            icon: 'O',
            tooltip: 'Visitar Optativas',
            onClick: (event, rowData) => navO(rowData)
        },
        {
            icon: 'E',
            tooltip: 'Visitar Especializante',
            onClick: (event, rowData) => navE(rowData)
        },
        {
            icon: 'P',
            tooltip: 'Visitar Proyectos Modulares',
            onClick: (event, rowData) => navP(rowData)
        }
    ]

    const accionesAdmin = [
        {
            icon: 'M',
            tooltip: 'Visitar materias',
            onClick: (event, rowData) => navM(rowData)
        },
        {
            icon: 'O',
            tooltip: 'Visitar Optativas',
            onClick: (event, rowData) => navO(rowData)
        },
        {
            icon: 'E',
            tooltip: 'Visitar Especializante',
            onClick: (event, rowData) => navE(rowData)
        },
        {
            icon: 'P',
            tooltip: 'Visitar Proyectos Modulares',
            onClick: (event, rowData) => navP(rowData)
        },
        {
            icon: 'X',
            tooltip: 'Eliminar',
            onClick: (event, rowData) => modificar(rowData)
        }
    ]



    const si = false;

    useEffect(() => {
        const fetchDegree = async () => {
          try {
            let url = `http://192.9.147.109/degree`;
            let response = await fetch(url);
            let data = await response.json();
            setDegree(data);
          } catch (error) {
            alert("Ha ocurrido un error al solicitar los datos");
          }
        };
        fetchDegree();
    }, []);

    const columnas =[
        {
            title:'Código',
            field:'degree_code'
            
        },
        {
            title:'Carrera',
            field:'degree_name'
        },
        {
            title:'Descripción',
            field:'degree_description'
        },
        {
            title:'Número de materias',
            field:'no_subjects',
            type: "numeric"
        },
    ]

    const navM = (props) => {
        navigate("/materias", { state: {rowData: props} })
    }
    
    const navO = (props) => {
        navigate("/optativas", { state: {rowData: props} })
    }

    const navE = (props) => {
        navigate("/especializantes", { state: {rowData: props} })
    }
    
    const navP = (props) => {
        navigate("/modulares", { state: {rowData: props} })
    }

    return (
        <div className="Fondo">
            <div className="relleno"/>
            <div className="Body">
                <h1>Carreras</h1>
                <div className="Parrafo">
                    La Universidad de Guadalajara atiende los requerimientos de formación profesional del estado de Jalisco a través de la red 
                    universitaria, que cuenta con seis centros universitarios temáticos ubicados en la zona metropolitana de Guadalajara y ocho 
                    centros regionales, así como un Sistema de Universidad Virtual, proporcionando una amplia gama de licenciaturas y programas 
                    de estudio profesionales.Esto permite la forja de profesionales altamente capacitados quienes se desempeñan en diversas áreas 
                    del conocimiento para beneficio de la sociedad.
                </div>
                <div>
                    <MaterialTable
                        columns={columnas}
                        data={degree}
                        title= 'Carreras en Wikimaterias'
                        actions={
                            tipo ? accionesUsuario : accionesAdmin
                        }
                        options={{
                            actionsColumnIndex: -1,
                        }}
                        localization={{
                            header:{
                                actions: 'Acciones'
                            }
                        }}
                    />
                </div>
            </div>
            <div className="relleno"></div>
        </div>    
    );
}

export default Carreras;