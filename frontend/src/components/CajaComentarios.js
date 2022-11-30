import React, { useState } from 'react';
import "./loginform.css"
import MenuFillIcon from 'remixicon-react/MenuFillIcon';
import {button} from 'react';
import carreras from './carreras';
import { useNavigate } from 'react-router-dom';
import { NavLink } from 'react-router-dom';
import "./CajaComentarios.css"
import Comentario from './comentario';
import { withTheme } from 'styled-components';
import { SafeAreaView, StyleSheet,TextInput } from 'react-native';
import StarRating from "./StarRating";
import ChangeRating from "./ChangeRating";
import "./Body.css";

const CajaComentarios = (props) => {


    const [Rankin,Comment] = useState({
        
    })

    const NombrePágina = props.name

    console.log("Si está entrando "+NombrePágina)
    
    const [avgRating, setAvgRating] = useState(0);

  const handleRating = (input) => {
    setAvgRating(input);
  };
    
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
    
    return(
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
                ></TextInput>
                <div className='ComentarioAcciones'>
                    <NavLink to='/Login' className="Comentar-btn">
                        Comentar
                    </NavLink>
                </div>
                {
                    Comentarios.map((comentario, index) => 
                    {
                        return(<Comentario key={index} usuario={comentario.usuario} comentario_contenido={comentario.comentario_contenido} ranking={comentario.ranking}/>)
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


export default CajaComentarios