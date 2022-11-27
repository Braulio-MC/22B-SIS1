import React, { useState, useEffect } from "react";
import "./carreras.css"
import "bootstrap/dist/css/bootstrap.min.css";
import "styled-components";
import DataTable from 'react-data-table-component';
import { Tooltip } from "bootstrap";
import MaterialTable from "material-table";
import { useLocation } from "react-router-dom";


const Materias = () => {
    const location = useLocation();
    const [subject, setSubject] = useState();
    const state =  location.state.rowData

    useEffect(() => {
        const fetchSubject = async () => {
          try {
            let degree_code = state.degree_code;
            let url = `http://192.9.147.109/subject/${degree_code}`;
            let response = await fetch(url);
            let data = await response.json();
            setSubject(data);
          } catch (error) {
            alert("Ha ocurrido un error al solicitar los datos");
          }
        };
        fetchSubject();
    }, []);

    console.log(subject);

    const TablaCarreras =[
        {degree_code: 1, degree_name: "Carrera 1", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
        {degree_code: 2, degree_name: "Carrera 2", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
        {degree_code: 3, degree_name: "Carrera 3", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
    ]

    const columnasMaterias =[
        {name: 'CVE', selector: 'cve', sorteable: true},
        {name: 'Codigo de carrera', selector: 'degree_code', sorteable: true},
        {name: 'Descripción', selector: 'degree_description', sorteable: true},
        {name: 'Acciones', sorteable: true}
    ]

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

    const nav = (props) => {
        console.log(props)
    }

    return(
        <div >
            <div className="relleno"></div>
            <div>
                <h1>Materias de {state.degree_name}</h1>
                <div className="Parrafo">
                    </div>
                    <div>
                        <MaterialTable
                            columns={columnas}
                            data={TablaCarreras}
                            title= 'Materias'
                            actions={[
                                {
                                icon: 'M',
                                tooltip: 'Materias',
                                
                                onClick: (event, rowData) => nav(rowData)
                                }
                            ]}
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
            
                <div className="buttonStandar">
                    Botón
                </div>
            </div>
            <div className="relleno">   
            </div>
        </div>    
    )
}

export default Materias