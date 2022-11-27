import React, { useState, useEffect } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import MaterialTable from "material-table";
import { useNavigate } from "react-router-dom";


const Modulares = () => {
    const navigate = useNavigate();
    const [modular, setModular] = useState([]);

    useEffect(() => {
        const fetchModular = async () => {
          try {
            let url = `http://192.9.147.109/modular`;
            let response = await fetch(url);
            let data = await response.json();
            setModular(data);
          } catch (error) {
            alert("Ha ocurrido un error al solicitar los datos");
          }
        };
        fetchModular();
    }, []);

    const TablaCarreras = [
        {degree_code: 1, degree_name: "Carrera 1", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
        {degree_code: 2, degree_name: "Carrera 2", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
        {degree_code: 3, degree_name: "Carrera 3", degree_description: "Descripción", no_subjects: 15, no_semesters: 8, last_update_date: "15/03/2021"},
    ]

    const columnas =[
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
            title:'Código de proyecto modular',
            field:'modular_project_code'
        },
        {
            title:'Descripción',
            field:'modular_project_description'
        },
    ]

    const nav = (props) => {
        navigate("/modular", { state: {rowData: props} })
    }

    return (
        <div >
            <div className="relleno"></div>
            <div>
                <h1>Proyectos modulares</h1>
                <div className="Parrafo"></div>
                <div>
                    <MaterialTable
                        columns={columnas}
                        data={modular}
                        title= 'Proyectos modulares en Wikimaterias'
                        actions={[
                            {
                                icon: 'M',
                                tooltip: 'Visitar modular',
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

export default Modulares;