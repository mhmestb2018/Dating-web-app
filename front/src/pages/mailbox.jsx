import React, { FunctionComponent, useState, useEffect } from 'react';
import User from '../models/user';

//import formatDate from '../helpers/format-date'

import { useHistory } from 'react-router-dom'

import Loader from 'react-loader-spinner'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"

import axios from 'axios';


const Mailbox = () => {
    //const [users, setUSers] = useState([]);

    const [Matches, setMatches] = useState([]);
    const [newMessage, setNewMessage] = useState("");
    const [userSelected, setUserSelected] = useState({});
  

const get_match = () => {
    axios
    .get("/matches")
    .then((res) => {
      //console.log("SuCcEsS:");
      console.log(res.users)
      setMatches(res.data.users);
      if (res.data.users[0])
      {
        //alert(`Get user ${res.data.users[0].first_name}`)
        setUserSelected(res.data.users[0])
        axios
        .get("/conversations")
        .then((res) => {
          alert('res')
        })
        .catch((err) => {
          alert('err')
        })
        
      }
    })
    .catch(function (error) {
      console.log(error);
      //alert("error_get_users");
    });
  }

  const get_conversations = (path) => {
    axios
    .get(path)
    .then((res) => {
      //console.log("SuCcEsS:");
      console.log(res)
      alert('SUCCESS')
      //setUSers(res.data.users);
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
      alert('SUCCESS')
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
            <div class="card-header" style={{textAlign: "center"}}>Messagerie</div>

      <div className="row">
        <div className="col-lg-3" style={{ top: "50px" }}>
          <div className="list-group" style={{ paddingBottom: "15px" }}>
            {
              Matches.map(match => {
                //alert(match.first_name);
                  return <div className="card" onClick={() => {setUserSelected(match)}}><div className="card-body">{match.first_name}</div></div>
              })
            }
          </div>
        </div>
        <div className="col-lg-9" style={{ top: "50px" }}>
          <div className="card">
            <div className="card-body">
                Messages
            <div style={{  border: "2px solid #dedede", backgroundColor: "#f1f1f1", borderRadius: "5px", padding: "10px", margin: "10px 0"}}>
              {/*<img src="/w3images/bandmember.jpg" alt="Avatar" style="width:100%;"/>*/}
              <p>Hello. How are you today?</p>
              <span >11:00</span>
            </div>
            <div style={{  border: "2px solid #ccc", backgroundColor: "#ddd", borderRadius: "5px", padding: "10px", margin: "10px 0"}}>
              {/*<img src="/w3images/bandmember.jpg" alt="Avatar" style="width:100%;"/>*/}
              <p>Hello, I'm fine</p>
              <span >12:00</span>
            </div>
          <br/>
          <div className="input-group mb-3">
          <input type="text" className="form-control" value={newMessage} onChange={(e) => setNewMessage(e.target.value)} placeholder="Nouveau message .."/>
            <div className="input-group-append">
              <button className="btn btn-success" onClick={() => {alert(newMessage);send_message(newMessage);setNewMessage("")}} >Envoyer</button>
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