import React, { useState } from "react";
import "./carreras.css"
import "bootstrap/dist/css/bootstrap.min.css";
import "styled-components";
import DataTable from 'react-data-table-component';
import { Tooltip } from "bootstrap";
import MaterialTable from "material-table";


const Carreras = () => {

    const TablaCarreras =[
        {degree_code: 1, degree_name: "Carrera 1", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
        {degree_code: 2, degree_name: "Carrera 2", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
        {degree_code: 3, degree_name: "Carrera 3", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
    ]


    const ColumnasCarreras =[
        {name: 'Código', selector: 'degree_code', sorteable: true},
        {name: 'Nombre', selector: 'degree_name', sorteable: true},
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


    const Saludar = ()  => {
        alert("hola")
    }

    const viajar = (props) => {
        alert("Viajando pa lla"+props)
    }

    



    return(
   <div >
        <div className="relleno"></div>
        <div>
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
                        data={TablaCarreras}
                        title= 'Carreras CUCEI'
                        actions={[
                            {
                            icon: 'M',
                            tooltip: 'Materias',
                            
                            onClick: (event, rowData) => {
                                viajar(rowData.degree_code)
                            }
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
           
            <div className="buttonStandar" onClick={Saludar}>
                Botón
            </div>
        </div>
        <div className="relleno">   
        </div>
    </div>    
    )
}



export default Carreras