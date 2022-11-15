import React, { useState } from "react";
import "./loginform.css"

const Carreras = () => {

    const [popupStyle,showPopup] = useState("hide")

    const popup = ()  => {
        showPopup("login-popup")
        setTimeout(() => showPopup("hide"), 3000)
    }
    return(
   <div className="covertest">
            <div className="relleno">   
        </div>
        <div className="cover">
            <h1>Carreras</h1>
                <input type="text" placeholder="username" />
                <input type="password" placeholder="password" />
            <div className="login-btn" onClick={popup}>
                Login
            </div>
            <div className={popupStyle}>
                <h3>Login Failed</h3>
                <p>username or password incorrect</p>
            </div>

        </div>
        <div className="relleno">   
        </div>
    </div>    
    )
}

export default Carreras