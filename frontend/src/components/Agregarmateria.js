import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import CajaComentarios from "./CajaComentarios";
import "./Body.css"


const AgregarMateria = () => {
    const location = useLocation();
    const [subject, setSubject] = useState();
    const subjectRowData = location.state.rowData;

    /*useEffect(() => {
        const fetchSubject = async () => {
          try {
            let degree_code = subjectRowData.degree_code;
            let cve = subjectRowData.CVE
            let url = `http://192.9.147.109/subject/${degree_code}/${cve}`;
            let response = await fetch(url);
            let data = await response.json();
            setSubject(data);
          } catch (error) {
            alert("Ha ocurrido un error al solicitar los datos");
          }
        };
        fetchSubject();
    }, []);
 */

    

    console.log(subjectRowData)
    return (
      <div className="Fondo">
        <div className="Relleno"/>
       
           <form className="BodyF">
              <h1>Modificar {subjectRowData.subject_name}</h1>
              <h2>Ingrese los datos solictados</h2>
              <div className="divF">CVE:</div>
              <input className="inputF" type="text" defaultValue={subjectRowData.CVE} name="CVE"/>
              <div className="divF">Nombre de la materia:</div>
              <input className="inputF" type="text" defaultValue={subjectRowData.subject_name} name="subject_name"/>
              <div className="divF">Semestre:</div>
              <input className="inputF" type="text" defaultValue={subjectRowData.subject_semester} name="subject_semester"/>
              <div className="divF">Enlace de PDF:</div>
              <input className="inputF" type="text" defaultValue={subjectRowData.subject_description} name="subject_description"/>
              <div className="divF">Creditos:</div>
              <input className="inputF" type="text" defaultValue={subjectRowData.subject_credits} name="subject_credits"/>
              <div className="divF">Tipo:</div>
              <input className="inputF" type="text" defaultValue={subjectRowData.subject_type} name="subject_type"/>
              <br/><br/>
              <input type="submit" className="btn-form" value="Modificar" />
            </form> 
          
          <div className="Relleno"/>
 
        <div className="Relleno"/>
      </div>
    );
    
}

export default AgregarMateria;