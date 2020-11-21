import React, { FunctionComponent, useState, useEffect } from "react";
import { textChangeRangeIsUnchanged } from "typescript";


import Map from 'pigeon-maps'
import Marker from 'pigeon-marker'
import Overlay from 'pigeon-overlay'

import axios from 'axios';
const MyAccount = ({toast}) => {

    const [blocked_persons, setBlocked_persons] = useState([]);
    const [myProfile, setMyProfile] = useState(null);


    function mapTilerProvider (x, y, z, dpr) {
      return `https://a.tile.openstreetmap.org/${z}/${x}/${y}.png`
      // `https://a.tile.openstreetmap.fr/osmfr/${z}/${x}/${y}.png` pour une carte localisée fr (icone de baguette pour les boulangeries par exemple)
      // Dans les 2 cas, 3 serveurs existent, "a", "b" et "c" (début d'url), à vérifier si ça revient bien au même ou si y'a des différences de style/qualité
    }
    const unblock_person = (user_id, name) => {
        axios.post('/users/' + user_id,
        {
          "block" : false
        })
        .then(res => {
            console.log(res);
            console.log(res.data);
              toast.success("Vous avez bien débloqué " + name + " :)");
        })
        .catch(error => {
              // console.log(error.response.data);
              // console.log(error.response.status);
              //console.log(error);
              //alert(error.response.data.error)
          if (error.response.data)
            toast.error(error.response.data.error);
          else
            toast.error("Erreur de connection avec le serveur");
            //toast.error("error");
          });
    }

    const get_blocked_persons = () => {
        axios.get('/blocked')
        .then(res => {
            console.log(res);
            setBlocked_persons(res.data.users);
        })
        .catch(error => {
              // console.log(error.response.data);
              // console.log(error.response.status);
              //console.log(error);
              //alert(error.response.data.error)
            //toast.error("error");
          });
      }

  useEffect(() => {
    get_blocked_persons();
    axios.get('/profile')
    .then(res => {
      setMyProfile(res.data)
    })
    .catch(function (error) {
    });
  }, []);

  return (
    <div>
      <div className="container-fluid" style={{ top: "50px" }}>
        <br />
        <h1 style={{textAlign: "center"}}>Mon compte</h1>
        <br/>
        <div className="row" style={{ paddingBottom: "15px" }}>
          <div className="col-lg-6">
            <div className="list-group" style={{ paddingBottom: "15px" }}>
              <div className="card">
                <h5 className="card-title" style={{ textAlign: "center" }}>
                  Mes infos de connexion
                </h5>
                <div className="card-body">
                  <div className="row">
                    <div className="col-lg-4">Adresse email:</div>
                    <div className="col-lg-4">{myProfile && myProfile.email || "Aucune information ..."}</div>
                    <div className="col-lg-4" style={{ textAlign: "center" }}>
                      <button type="button" className="btn btn-success">
                        Modifier
                      </button>
                    </div>
                  </div>
                  <br />
                  <br />
                  <br />
                  <div className="row">
                    <div className="col-lg-4">Mot de passe:</div>
                    <div className="col-lg-4">********</div>
                    <div className="col-lg-4" style={{ textAlign: "center" }}>
                      <button type="button" className="btn btn-success">
                        Modifier
                      </button>
                    </div>
                  </div>
                  <br />
                  <br />
                </div>
              </div>
            </div>
          </div>
          <div className="col-lg-6">
            <div className="list-group" style={{ paddingBottom: "15px" }}>
              <div className="card">
                <h5 className="card-title" style={{ textAlign: "center" }}>
                  Mes personnes bloquées
                </h5>
                <div className="card-body">
                    {
                        blocked_persons.map((person) => {
                            return (
                                <div>
                                    <div className="row">
                            <div className="col-lg-6">{person.first_name}{" "}{person.last_name}</div>
                                            <div className="col-lg-6" style={{textAlign:"center"}}>
                                                <button type="button" onClick={() => unblock_person(person.id, person.first_name + " " + person.last_name)} className="btn btn-success">
                                                Débloquer
                                                </button>
                                            </div>
                                        </div>
                                    <br />
                                </div>
                            )
                        })
                    }
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="row">
            <div className="col-sm-12">
                <div className="list-group" style={{ paddingBottom: "15px"}}>
                    <div className="card">
                        <h5 className="card-title" style={{ textAlign: "center" }}>
                            Mes infos de connexion
                        </h5>
                        <div className="card-body" style={{textAlign:"center"}}>
                          {
                            myProfile &&
                          <Map center={[ myProfile.lat, myProfile.lon]} zoom={10} width={600} height={400} provider={mapTilerProvider} >
                            <Marker anchor={[myProfile.lat, myProfile.lon]} payload={1} onClick={({ event, anchor, payload }) => {}} />
                            <Overlay anchor={[myProfile.lat, myProfile.lon]} offset={[120, 79]}>
                            <img src='https://cdn.intra.42.fr/users/medium_pcachin.jpg' width={24} height={15} alt='' />
                            </Overlay>
                          </Map> ||
                            <div>Aucune info de connexion ...</div>
                          }
                            <br/>
                            <br/>
                            <br/>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <br />
      </div>
    </div>
  );
};

export default MyAccount;