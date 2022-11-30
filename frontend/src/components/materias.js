import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "styled-components";
import MaterialTable from "material-table";
import { useLocation, useNavigate } from "react-router-dom";
import MenuBookIcon from "@material-ui/icons/MenuBook";
import CajaComentarios from "./CajaComentarios";
import "./Body.css"
import "@material-ui/icons/MenuBook"    


const Materias = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [subject, setSubject] = useState([]);
    const degreeRowData =  location.state.rowData

    const comentarios = degreeRowData

    useEffect(() => {
        const fetchSubject = async () => {
            try {
                let degree_code = degreeRowData.degree_code;
                let url = `http://192.9.147.109/subject/${degree_code}`;
                let response = await fetch(url);
                let data = await response.json();
                data = data.filter((item) => {
                    return item["subject_type"] == "Regular";
                });
                setSubject(data);
            } catch (error) {
                alert("Ha ocurrido un error al solicitar los datos");
            }
        };
        fetchSubject();
    }, []);

    const TablaCarreras =[
        {degree_code: 1, degree_name: "Materia 1", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
        {degree_code: 2, degree_name: "Materia 2", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
        {degree_code: 3, degree_name: "Materia 3", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
    ]
    
    const columnasPlaceholder = [
        {title:"CVE", field:"CVE"},
        {title:"Nombre", field:"subject_name"},
        {title:"Créditos", field:"subject_credits", type:"numeric"},
        {title:"Semestre", field:"subject_semester", type:"numeric"},
    ]

    const columnas =[
        {
            title:'CVE',
            field:'CVE'
        },
        {
            title:'Código de carrera',
            field:'degree_code'
        },
        {
            title:'Última fecha de actualización',
            field:'last_update_date',
            type: 'date'
        },
        {
            title:'Créditos',
            field:'subject_credits',
            type: 'numeric'
        },
        {
            title: 'Descripción',
            field: 'subject_description'
        },
        {
            title: 'Nombre',
            field: 'subject_name'
        },
        {
            title: 'Semestre',
            field: 'subject_semester',
            type: 'numeric'
        },
        {
            title: 'Tipo',
            field: 'subject_type'
        }
    ]

    const nav = (props) => {
        navigate("/materia", { state: {rowData: props} })
    }

    return (
        <div className="Fondo">
            <div className="relleno"></div>
            <div className="Body">
                <h1>{degreeRowData.degree_name}</h1>
                <div className="Parrafo">
                    Esse anim laboris qui sit. Adipisicing commodo cillum velit Lorem ex. Dolor cupidatat pariatur sunt nisi nisi sit ullamco esse tempor laborum. Laborum magna sunt mollit qui elit. Qui sint adipisicing ex qui labore aliquip voluptate officia excepteur ad. Ad quis nisi dolor officia occaecat mollit est. Elit nisi sit reprehenderit ipsum eu nostrud laborum id ullamco quis velit excepteur exercitation irure.
                </div>
                <div>
                    <MaterialTable
                        columns={columnasPlaceholder}
                        data={subject}
                        title= {`Materias con código de carrera ${degreeRowData.degree_code}`}
                        actions={[
                            {
                                icon: MenuBookIcon,
                                tooltip: 'Visitar materia',
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
            </div>
            <div className="relleno"></div>
        </div>    
    );
}

export default Materias;