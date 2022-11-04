import React, { useState } from 'react';
import "./loginform.css"
import ToolBar from "./ToolBar";
import Sidebar from "./Sidebar";
import Backdrop from './Backdrop';

const Menu = () => {

    const[sidebar,setSidebar] = useState(false);

    const toggleSidebar = () =>{
        setSidebar((prevState) => !prevState)
    }

    return(
   <div>
        <ToolBar openSidebar={toggleSidebar}/>
        <Backdrop  sidebar={sidebar} closeSidebar={toggleSidebar}/>
        <Sidebar sidebar={sidebar}/>
    </div>  
    )
}

export default Menu