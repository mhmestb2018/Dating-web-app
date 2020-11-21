import React, { FunctionComponent, useState, useEffect } from 'react';
import User from '../models/user';

//import formatDate from '../helpers/format-date'

import { useHistory } from 'react-router-dom'

import Loader from 'react-loader-spinner'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"

import axios from 'axios';


const Mailbox = () => {
    //const [users, setUSers] = useState([]);

    const [conversations, setConversations] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const [messages, setMessages] = useState([]);
    const [userSelected, setUserSelected] = useState({});
  

  const get_match = () => {
    axios
    .get("/matches")
    .then((res) => {
      console.log("/matches")
      console.log(res)
      setConversations(res.data.users);
      if (res.data.users[0])
      {
        setUserSelected(res.data.users[0])
        get_messages(res.data.users[0].id)
      }
    })
    .catch((err) => {
      alert('err')
    })
  }

  const get_conversations = (path) => {
    axios
    .get(path)
    .then((res) => {
      console.log("SuCcEsS:");
      console.log(res)
      //setUSers(res.data.users);
    })
    .catch(function (error) {
      console.log(error);

      alert('error')
      //alert("error_get_users");
    });
  }


  const get_messages = (userId) => {
    axios
    .post("/messages", {"user":userId})
    .then((res) => {
      console.log("/messages:");
      console.log(res)
      //setUSers(res.data.users);
      setMessages(res.data.messages)
    })
    .catch(function (error) {
      console.log(error);

      alert('error')
      //alert("error_get_users");
    });
  }

  const send_message = (message) => {
    axios
    .post("/new_message",
    {
      user: userSelected.id,
      content: message
    })
    .then((res) => {
      //console.log("SuCcEsS:");
      console.log(res)
      get_messages(userSelected.id)
      //setUSers(res.data.users);
    })
    .catch(function (error) {
      console.log(error);

      alert('error')
      //alert("error_get_users");
    });
  }

  
    useEffect(() => {
      (async function () {
        get_match()
        get_conversations("/conversations");
      })();
    }, []);

  return (
    <div className="container-fluid">

      <div className="row">
        <div className="col" style={{ top: "50px" }}>
            <div className="card">
              <div className="card-body">
            <div className="card-header" style={{textAlign: "center"}}>Messagerie</div>

      <div className="row">
        <div className="col-lg-3" style={{ top: "50px" }}>
          <div className="list-group" style={{ paddingBottom: "15px" }}>
            {
              conversations.map(conversation => {
                //alert(match.first_name);
              return <div className="card" key={conversation.id} onClick={() => {setUserSelected(conversation);get_messages(conversation.id)}}><div className="card-body">{conversation.first_name}</div></div>
              })
            }
          </div>
        </div>
        <div className="col-lg-9" style={{ top: "50px" }}>
          <div className="card">
            <div className="card-body">
                Messages
          <br/>
          {
            
            messages.map(message => {
              //alert(match.first_name);
                //return <div className="card" key={message.date}><div className="card-body">{message.content}</div></div>
                if (message.from == userSelected.id)
                return (
                  <div key={message.date} style={{ textAlign:"right", border: "2px solid #dedede", backgroundColor: "#f1f1f1", borderRadius: "5px", padding: "10px", margin: "10px 0"}}>
                  {/*<img src="/w3images/bandmember.jpg" alt="Avatar" style="width:100%;"/>*/}
                  <p>{message.content}</p>
                  <span >{message.date}</span>
                </div>
                )
                else
                  return (
                    <div key={message.date} style={{  border: "2px solid #ccc", backgroundColor: "#ddd", borderRadius: "5px", padding: "10px", margin: "10px 0"}}>
                    {/*<img src={userSelected.user.pictures[0]} alt="Avatar" style="width:100%;"/>*/}
                    <p>{message.content}</p>
                    <span >{message.date}</span>
                  </div>
                  )
            })
          }
          <br/>
          <div className="input-group mb-3">
          <input type="text" className="form-control" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} placeholder="Nouveau message .."/>
            <div className="input-group-append">
              <button className="btn btn-success" disabled={(newMessage == 0? true: false)} onClick={() => {send_message(newMessage);setNewMessage("")}} >Envoyer</button>
            </div>
          </div>
          </div>
          </div>
        </div>
      </div>
      <br/>
      <br/>
      <br/>
      </div>
      </div>
      </div>
      </div>
    </div>
  );
}

export default Mailbox;