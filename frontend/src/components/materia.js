import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

const Materia = () => {
    const location = useLocation();
    const [subject, setSubject] = useState();
    const subjectRowData = location.state.rowData;

    useEffect(() => {
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

    
}

export default Materia;