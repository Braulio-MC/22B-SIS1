import React, { useState } from 'react';
import "./loginform.css"
import ToolBar from "./ToolBar";
import Sidebar from "./Sidebar";
import Backdrop from './Backdrop';
import MenuFillIcon from 'remixicon-react/MenuFillIcon';
import {button} from 'react';


const Menu = () => {


    return(
        <div>
        <div className="tool-bar">
            <div className="burger">
                <i><MenuFillIcon/></i>
            </div>
            <a href='/'> Menú</a>
            <a href='/carreras'> Carreras</a>
            <a href='/login'>Login</a>
        </div>
            

    </div>
    )
}

export default Menu