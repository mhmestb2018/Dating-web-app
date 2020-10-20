/* eslint-disable */
import React, { FunctionComponent, useState, useEffect } from "react";
import User from "../models/user";
//import USER_LIST from '../models/mock-user';
import UserCard from "../components/user-card";
import getGenderColor from "../helpers/get-gender-color";

import Map from 'pigeon-maps'
import Marker from 'pigeon-marker'
import Overlay from 'pigeon-overlay'

import axios from "axios";

const UserList = () => {
  const [users, setUSers] = useState([]);


  const [ageMin, setAgeMin] = useState(18);
  const [ageMax, setAgeMax] = useState(100);
  const [scoreMin, setScoreMin] = useState(0);
  const [scoreMax, setScoreMax] = useState(100);
  const [distanceMax, setDistanceMax] = useState(50000);
  const [tags, setTags] = useState("");


const get_user_list = (path) => {
  axios
  .get(path)
  .then((res) => {
    //console.log("SuCcEsS:");
    console.log(res)
    setUSers(res.data.users);
  })
  .catch(function (error) {
    console.log(error);
    //alert("error_get_users");
  });
}

const get_custom_user_list = (path) => {
  axios.post(path,
    {
      "age":{
        "min": ageMin,
        "max": ageMax
      },
      "score" : {
        "min": scoreMin,
        "max": scoreMax
      },
      "distance": distanceMax,
      "tags" : tags.split(' ') == "" ? [] : tags.split(' ')
    })
  .then((res) => {
    //console.log("SuCcEsS:");
    console.log(res)
    setUSers(res.data.users);
  })
  .catch(function (error) {
    console.log(error);
    //alert("error_get_users");
  });
}

  useEffect(() => {
    (async function () {
      get_custom_user_list("/users");
    })();
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(getPosition);
    }
  }, []);
  function getPosition(position) {
    setGeoloc_pos(Array(position.coords.latitude, position.coords.longitude))
  }


  //const [users, setUSers] = useState([]);
  useEffect(() => {
    (async function () {
      get_user_list("/matches");
    })();
  }, []);

  const [geoloc_pos, setGeoloc_pos] = useState([]);
  const [frame, setFrame] = useState(0);



  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-lg-3" style={{ top: "50px" }}>
          <div className="list-group" style={{ paddingBottom: "15px" }}>
            <div className="card">
              <div className="card-body">
                <div id="menulinks" className="nav nav-pills">
                  <a style={{ width: "100%" }} className="nav-link ">
                    <i className="fa fa-home" aria-hidden="true"></i> Age min:
                    {ageMin}
                  </a>
                  <div className="row">
                    <div className="col-4">18</div>
                    <div className="col-4">
                      <input
                        type="range"
                        min="18"
                        max="100"
                        className="custom-range"
                        value={ageMin}
                        onChange={(e) => setAgeMin(parseInt(e.target.value))}
                      ></input>
                    </div>
                    <div className="col-4">100</div>
                  </div>
                  <a style={{ width: "100%" }} className="nav-link ">
                    <i className="fa fa-line-chart" aria-hidden="true"></i> Age max: {ageMax}
                  </a>
                  <div className="row">
                    <div className="col-4">18</div>
                    <div className="col-4">
                      <input
                        type="range"
                        min="18"
                        max="100"
                        className="custom-range"
                        value={ageMax}
                        onChange={(e) => setAgeMax(parseInt(e.target.value))}
                      ></input>
                    </div>
                    <div className="col-4">100</div>
                  </div>
                  <a style={{ width: "100%" }} className="nav-link ">
                    <i className="fa fa-suitcase" aria-hidden="true"></i>{" "}
                    Popularité min: {scoreMin}
                  </a>

                  <div className="row">
                    <div className="col-4">0</div>
                    <div className="col-4">
                      <input
                        type="range"
                        min="0"
                        max="100"
                        className="custom-range"
                        value={scoreMin}
                        onChange={(e) => setScoreMin(parseInt(e.target.value))}
                      ></input>
                    </div>
                    <div className="col-4">100</div>
                  </div>
                  <a style={{ width: "100%" }} className="nav-link ">
                    <i className="fa fa-sign-out" aria-hidden="true"></i>{" "}
                    Popularité max: {scoreMax}
                  </a>

                  <div className="row">
                    <div className="col-4">0</div>
                    <div className="col-4">
                      <input
                        type="range"
                        min="0"
                        max="100"
                        className="custom-range"
                        value={scoreMax}
                        onChange={(e) => setScoreMax(parseInt(e.target.value))}
                      ></input>
                    </div>
                    <div className="col-4">100</div>
                  </div>
                  <div className="row">
                    <div className="col-5">Distance max</div>
                    <div className="col-7"><input value={distanceMax} onChange={(e) => setDistanceMax(parseInt(e.target.value))} type="text"></input></div>
                  </div>
                  <br/>
                  <div className="row">
                    <div className="col-5">Tags</div>
                    <div className="col-7"><input value={tags} onChange={(e) => setTags(e.target.value)} type="text"></input></div>
                  </div>
                  <div className="row">

                  <div className="col-12">
                    <button type="button" onClick={() => get_custom_user_list("/users")} className="btn btn-success">Enregistrer</button>
                  </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="col-lg-9" style={{ top: "50px" }}>
          <div className="card">
            <div className="card-body">
            <ul className="nav nav-tabs">
              <li className="nav-item">
                <a className={frame == 0 ? "nav-link active" : "nav-link"} style={{cursor: "pointer"}} onClick={() => {setFrame(0);get_custom_user_list("/users")}}>Vue globales</a>
              </li>
              <li className="nav-item">
                <a className={frame == 1 ? "nav-link active" : "nav-link"} style={{cursor: "pointer"}} onClick={() => {setFrame(1);get_user_list("/matches")}}>Mes matchs</a>
              </li>
              <li className="nav-item">
                <a className={frame == 2 ? "nav-link active" : "nav-link"} style={{cursor: "pointer"}} onClick={() => setFrame(2)} >Carte</a>
              </li>
              <li className="nav-item">
                <a className={frame == 3 ? "nav-link active" : "nav-link"} style={{cursor: "pointer"}} onClick={() => {setFrame(3);get_user_list("/liked_by")}} >Mes likes</a>
              </li>
              <li className="nav-item">
                <a className={frame == 4 ? "nav-link active" : "nav-link"} style={{cursor: "pointer"}} onClick={() => {setFrame(4);get_user_list("/users")}} >Mes personnes blockées</a>
              </li>
            </ul> 
            <br/>
            {
              frame == 0 ?
              <div className="row">
                {users && users.map((user) => (
                      <UserCard user={user} key={user.id} borderColorHover={getGenderColor(user.sex)}/>
                    )
                  )  || <div>No UsEr !</div>
                }
              </div>
              : frame == 1 ?
              <div className="row">
                {users && users.map((user) => (
                      <UserCard user={user} key={user.id} borderColorHover={getGenderColor(user.sex)}/>
                    )
                  )  || <div>No UsEr !</div>
                }
              </div>
              : frame == 2 ?
                <Map center={geoloc_pos} zoom={12} width={600} height={400}>
                <Marker anchor={geoloc_pos} payload={1} onClick={({ event, anchor, payload }) => {}} />
            
                <Overlay anchor={geoloc_pos} offset={[120, 79]}>
                  <img src='https://cdn.intra.42.fr/users/medium_pcachin.jpg' width={24} height={15} alt='' />
                </Overlay>
              </Map>
              : frame == 3 ?
              <div className="row">
                {users && users.map((user) => (
                      <UserCard user={user} key={user.id} borderColorHover={getGenderColor(user.sex)}/>
                    )
                  )  || <div>No UsEr !</div>
                }
              </div>
              :
              <div className="row">
                {users && users.map((user) => (
                      <UserCard user={user} key={user.id} borderColorHover={getGenderColor(user.sex)}/>
                    )
                  )  || <div>No UsEr !</div>
                }
              </div>
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserList;
