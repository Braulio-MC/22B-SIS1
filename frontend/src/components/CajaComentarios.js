import React, { useState, useEffect } from 'react';
import "./loginform.css"
import { NavLink } from 'react-router-dom';
import "./CajaComentarios.css"
import Comentario from './comentario';
import { StyleSheet,TextInput } from 'react-native';
import StarRating from "./StarRating";
import ChangeRating from "./ChangeRating";
import "./Body.css";


const CajaComentarios = (props) => {
    const subjectData = props.subjectRowData;
    const [avgRating, setAvgRating] = useState(0);
    const [comentarios, setComentarios] = useState([]);
    const [comentarioNuevo, setComentarioNuevo] = useState({
        cve: subjectData.CVE,
        student_code: sessionStorage.getItem('student_code'),
        commentary: "",
        grade: 0
    });

    const handleRating = (input) => {
        setAvgRating(input);
        input = Number(input);
        setComentarioNuevo({
            ...comentarioNuevo,
            grade: input
        });
    };
    
    useEffect(() => {
        const fetchComentarios = async () => {
            try {
                let cve = subjectData.CVE
                let url = `http://192.9.147.109/subject-comments/${cve}`;
                let response = await fetch(url);
                let data = await response.json();
                setComentarios(data);
            } catch (error) {
              alert("Ha ocurrido un error al obtener los comentarios");
            }
        };
        fetchComentarios();
    }, []);

    const AgregarComentario = async () => {
        try {
            let url = `http://192.9.147.109/subject-comments`;
            let headers = {
                "Content-Type": "application/json",
                "X-Access-Token": sessionStorage.getItem('accessToken')
            };
            let response = await fetch(url, {
                method: 'POST', 
                headers: headers,
                body: JSON.stringify(comentarioNuevo)
            });
            let message = await response.json();
            alert(message["message"]);
        } catch (error) {
          alert("Ha ocurrido un error al publicar el comentario");
        }
    };

    const validaDatos = () => {
        let c = comentarioNuevo.commentary;
        let g = comentarioNuevo.grade;
        if (c.length == 0 || (g < 0 || g > 5))
            return false;
        return true;
    }

    const handleOnClick = () => {
        if (validaDatos()) {
            AgregarComentario();
            
        } else {
            alert("Comentario vacio o calificacion invalida");
        }
    }

    const handleOnChange = (event) => {
        setComentarioNuevo({
            ...comentarioNuevo,
            commentary: event.target.value
        });
    }

    const Comentarios = [
        {usuario:"Juan 1",comentario_contenido:"Officia deserunt reprehenderit commodo deserunt magna excepteur Lorem occaecat officia id laborum est reprehenderit cillum. Consectetur sint occaecat incididunt Lorem eiusmod magna nisi dolor officia. Sunt non veniam et in labore aliquip exercitation velit.",ranking:3},
        {usuario:"Juan2",comentario_contenido:"Está chevere 2",ranking:4},
        {usuario:"Juan3",comentario_contenido:"Está chevere 3",ranking:5},
    ]

    const MediaRanking=()=>{
        for (let index = 0; index < Comentarios.length; index++) {
            const element = Comentarios[index];
            
        }
    }
    
    return (
        <div className='ContenedorCaja'>
            <div>
                Caja de comentarios
            </div>
            <div className="App">
                <StarRating stars={avgRating} />
                <br />
                <br />
                <ChangeRating rating={avgRating} handleRating={handleRating} />
            </div>
            <div className='Caja'>
                <TextInput
                    style={styles.multiline}
                    placeholder='Comenta tu opinión...'
                    multiline={true}
                    numberOfLines={4}
                    onChange={handleOnChange}
                    maxLength={400}
                ></TextInput>
                <div className='ComentarioAcciones'>
                    {sessionStorage.getItem('accessToken') 
                        ? <div className='Comentar-btn' onClick={handleOnClick}>Comentar</div>
                        : <NavLink to='/login' className="Comentar-btn">Autenticar</NavLink>
                    }
                </div>
                {
                    comentarios.map((comentario, index) => 
                    {
                        return (
                            <Comentario 
                                key={index} 
                                usuario={comentario.student_code} 
                                comentario_contenido={comentario.commentary} 
                                ranking={comentario.grade}
                            />
                        );
                    })
                }
            </div>
        </div>
    )
}

const styles = StyleSheet.create({
    multiline: {
        padding: 4,
        marginVertical: '1rem',
        width: '90%',
        backgroundColor: 'white',
    }
});


export default CajaComentarios;