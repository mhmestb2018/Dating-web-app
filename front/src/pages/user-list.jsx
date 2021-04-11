/* eslint-disable */
import React, { FunctionComponent, useState, useEffect } from "react";
import User from "../models/user";

import Select from 'react-select';
import makeAnimated from 'react-select/animated';
//import USER_LIST from '../models/mock-user';
import UserCard from "../components/user-card";
import getGenderColor from "../helpers/get-gender-color";

import Map from 'pigeon-maps'
import Marker from 'pigeon-marker'
import Overlay from 'pigeon-overlay'

import axios from "axios";


import { useContext } from 'react';
import { AppContext } from '../App.jsx';

const animatedComponents = makeAnimated();

const UserList = () => {
  const [users, setUSers] = useState([]);
  const [profile, setProfile] = useState([]);

  const context_value = useContext(AppContext);


  const [allTags, setAllTags] = useState([]);
  const [selectedTags, setSelectedTags] = useState([]);

  const [ageMin, setAgeMin] = useState(18);
  const [ageMax, setAgeMax] = useState(100);
  const [scoreMin, setScoreMin] = useState(0);
  const [scoreMax, setScoreMax] = useState(100);
  const [distanceMax, setDistanceMax] = useState(50000);
  const [tags, setTags] = useState("");

  const colourOptions = [
    { value: 'ocean', label: 'Ocean', color: '#00B8D9', isFixed: true },
    { value: 'blue', label: 'Blue', color: '#0052CC', isDisabled: true },
    { value: 'purple', label: 'Purple', color: '#5243AA' },
    { value: 'red', label: 'Red', color: '#FF5630', isFixed: true },
    { value: 'orange', label: 'Orange', color: '#FF8B00' },
    { value: 'yellow', label: 'Yellow', color: '#FFC400' },
    { value: 'green', label: 'Green', color: '#36B37E' },
    { value: 'forest', label: 'Forest', color: '#00875A' },
    { value: 'slate', label: 'Slate', color: '#253858' },
    { value: 'silver', label: 'Silver', color: '#666666' },
  ];


  const get_all_tags = () => {
    axios
    .get("/tags")
    .then((res) => {
      console.log(res.data.tags)
      let tmp = []
      res.data.tags.map(tag => {
        tmp.push({value:tag, label:tag, color:""})
      })
      setAllTags(tmp);
    })
    .catch(function (error) {
      console.log(error);
    });
  }

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
      "tags" : selectedTags
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

function get_profile()//RECUPERE LA POSITION DU USER ET TOUT !
{
  axios.get("/profile")
  .then((res) => {
    //console.log("SuCcEsS:");
    console.log(res)
    setUSers(res.data.users);
    const [profile, setProfile] = useState(null);
  })
  .catch(function (error) {
    console.log(error);
    //alert("error_get_users");
  });
}

  //const [users, setUSers] = useState([]);
  useEffect(() => {
    (async function () {
      get_custom_user_list("/users")
      get_all_tags()
    })();
  }, []);

  const [frame, setFrame] = useState(0);


  function mapTilerProvider (x, y, z, dpr) {
    return `https://a.tile.openstreetmap.org/${z}/${x}/${y}.png`
    // `https://a.tile.openstreetmap.fr/osmfr/${z}/${x}/${y}.png` pour une carte localisée fr (icone de baguette pour les boulangeries par exemple)
    // Dans les 2 cas, 3 serveurs existent, "a", "b" et "c" (début d'url), à vérifier si ça revient bien au même ou si y'a des différences de style/qualité
  }
  return (
    <div className="container-fluid">
      <div className="row" style={{textAlign:"center"}}>
        {
          context_value.pictures.length > 0 &&
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
                        <br/>
                      </div>
                      <br/>
                      <div className="row" style={{width:"100%"}}>
                        <div className="col-12" style={{textAlign:"center"}}>Distance max</div>
                        <br/>
                      </div>
                      <div className="row" style={{width:"100%"}}>
                        <div className="col-12"><input value={distanceMax} onChange={(e) => setDistanceMax(parseInt(e.target.value))} type="text"></input></div>
                        <br/>
                      </div>
                      <br/>
                      <div className="row" style={{width:"100%"}}>
                        <div className="col-12">
                          <Select
                          closeMenuOnSelect={false}
                          components={animatedComponents}
                          //defaultValue={[colourOptions[4], colourOptions[5]]}
                          isMulti
                          options={allTags}
                          //options={colourOptions}
                          onChange={(values) => {let tmp = [];if (values) values.map(value => {tmp.push(value.value)});setSelectedTags(tmp)}}
                        />
                        <br/>
                      </div>
                      <br/>
                      </div>
                      <br/>
                      <br/><br/>
                      <div className="row">
                        <br/>
                        <div className="col-12">
                          <button style={{textAlign:"center"}} type="button" onClick={() => get_custom_user_list("/users")} className="btn btn-success">Enregistrer</button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
        }

        <div className="col" style={{ top: "50px" }}>
          <div className="card">
            <div className="card-body">
            <ul className="nav nav-tabs">
              <li className="nav-item">
                <a className={frame == 0 ? "nav-link active" : "nav-link"} style={{cursor: "pointer"}} onClick={() => {setFrame(0);get_custom_user_list("/users")}}>Vue globales</a>
              </li>
              <li className="nav-item">
                <a className={frame == 5 ? "nav-link active" : "nav-link"} style={{cursor: "pointer"}} onClick={() => {setFrame(5);get_user_list("/visits")}} >Mes visites</a>
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
                <a className={frame == 4 ? "nav-link active" : "nav-link"} style={{cursor: "pointer"}} onClick={() => {setFrame(4);get_user_list("/blocked")}} >Mes personnes blockées</a>
              </li>
            </ul> 
            <br/>
            {
              frame == 2 ?
              <Map center={[49.5167, 5.7667]} zoom={10} width={600} height={400} provider={mapTilerProvider} >
                <Marker anchor={[49.5167, 5.7667]} payload={1} onClick={({ event, anchor, payload }) => {}} />
                <Overlay anchor={[49.5167, 5.7667]} offset={[120, 79]}>
                <img src='https://cdn.intra.42.fr/users/medium_pcachin.jpg' width={24} height={15} alt='' />
                </Overlay>
              </Map>
              /*
                <Map center={geoloc_pos} zoom={10} width={600} height={400} provider={mapTilerProvider}  dprs={[1, 2]} >
                <Marker anchor={geoloc_pos} payload={1} onClick={({ event, anchor, payload }) => {}} />
            
                <Overlay anchor={geoloc_pos} offset={[120, 79]}>
                  <img src='https://cdn.intra.42.fr/users/medium_pcachin.jpg' width={24} height={15} alt='' />
                </Overlay>
              </Map>*/
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
