import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

const Modular = () => {
    const location = useLocation();
    const [modular, setModular] = useState();
    const modularRowData = location.state.rowData;

    /* useEffect(() => {
        const fetchModular = async () => {
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
        fetchModular();
    }, []); */
    
}

export default Modular;