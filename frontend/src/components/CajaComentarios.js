import React, { useState } from 'react';
import "./loginform.css"
import MenuFillIcon from 'remixicon-react/MenuFillIcon';
import { SafeAreaView, StyleSheet, TextInput } from "react-native";
import {button} from 'react';
import carreras from './carreras';
import { useNavigate } from 'react-router-dom';
import { NavLink } from 'react-router-dom';
import "./CajaComentarios.css"
import Comentario from './comentario';
import { withTheme } from 'styled-components';


const CajaComentarios = (props) => {

    const NombrePágina = props.name

    console.log("Si está entrando "+NombrePágina)

    
    const Comentarios = [
        {usuario:"Juan 1",comentario_contenido:"Está chevere 1",ranking:3},
        {usuario:"Juan2",comentario_contenido:"Está chevere 2",ranking:4},
        {usuario:"Juan3",comentario_contenido:"Está chevere 3",ranking:5},
    ]

    
    
    return(
        <div className='ContenedorCaja'>
            <div>
                Caja de comentarios
            </div>
            <div className='Caja'>
                <TextInput
                    style={styles.multiline}
                    placeholder='Comenta tu opinión...'
                    multiline={true}
                    numberOfLines={4}
                ></TextInput>
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