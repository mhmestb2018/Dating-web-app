import React, { FunctionComponent, useState  } from "react";

function Chat_widget() {
    const [chat_display, setChat_display] = useState("none");

    const openButton = {
        backgroundColor: "#555",
        color: "white",
        border: "none",
        cursor: "pointer",
        opacity: "0.8",
        position: "fixed",
        bottom: "0px",
        right: "0px"
    }

    const modal_popup = {
        display: chat_display, /* Hidden by default */
        position: "fixed", /* Stay in place */
        zIndex: "1", /* Sit on top */
        left: "0",
        top: "0",
        width: "100%", /* Full width */
        height: "100%", /* Full height */
        overflow: "auto", /* Enable scroll if needed */
        backgroundColor: "rgb(0,0,0)", /* Fallback color */
        backgroundColor: "rgba(0,0,0,0.4)",
    }
    const modal_content = {
        position: "fixed",
        right: "0",
        backgroundColor: "#fefefe",
        heigth: "100%"
    }
    const modal_header = {
        padding: "2px 16px",
        backgroundColor: "#5cb85c",
        color: "white"
    }
    const modal_body = {padding: "2px 16px"}
    return (
        <div >
            <div id="myModal" style={modal_popup}>
                <div style={modal_content}>
                <div style={modal_header}>
                    {/*<span class="close">&times;</span>*/}
                    <h2>Modal Header</h2>
                    <h2 onClick={() => setChat_display(chat_display == "none" ? "block" : "none")}>Fermer</h2>
                </div>
                <div style={modal_body}>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                    <p>User0</p>
                    <p>User1</p>
                </div>
                {/*<div class="modal-footer">
                    <h3>Modal Footer</h3>
                </div>*/}
                </div>
            </div>
            <button style={openButton} onClick={() => setChat_display(chat_display == "none" ? "block" : "none")}> Messagerie instantanée </button>
        </div>
    )
}

export default Chat_widget;