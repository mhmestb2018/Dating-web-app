import React, { FunctionComponent, useState, useEffect } from "react";
//import formatDate from '../helpers/format-date'
import { useHistory } from "react-router-dom";

import Loader from "react-loader-spinner";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";

const User_page = ({ user, my_profile, loader, detail, get_user }) => {

  const history = useHistory();
  const [first_picture, setFirst_picture] = useState("");

  if (first_picture == "" && user && user[0] && user[0].pictures[0])
    setFirst_picture(user[0].pictures[0])

  return (
    <div>
      {!loader && user[0] ? (
        <div className="row">
          <div className="col s12 m8 offset-m2">
            {
              detail ?
              <h2 className="header center" style={{ textAlign: "center" }}>
                {user[0].first_name} {user[0].last_name ? user[0].last_name : ""}
              </h2>
              :
              <div className="row">
                <div className="col-sm-6 col-lg-6" style={{textAlign:"center"}}>
                  Prénom: <input onChange={(e) => {my_profile.setFirst_name(e.target.value);my_profile.setIsmodify(true)}} type="text" value={user[0].first_name}/>
                </div>
                <div className="col-sm-6 col-lg-6" style={{textAlign:"center"}}>
                  Nom: <input onChange={(e) => {my_profile.setLast_name(e.target.value);my_profile.setIsmodify(true)}} type="text" value={user[0].last_name}/>
                </div>
              </div>
            }
            <div className="card">
              <div className="card-body">
                <div className="card-image">
                  <img
                    src={first_picture}
                    alt={first_picture}
                    style={{
                      display: "block",
                      marginLeft: "auto",
                      marginRight: "auto",
                      width: "50%",
                    }}
                  />
                </div>
                <div className="row">
                  <div className="col-sm-4 col-lg-4"> </div>
                  <div className="col-sm-4 col-lg-4">
                    <div className="d-flex">
                      {user[0].pictures.map(function (picture) {
                        return (
                          <div key={picture} className="p-2 flex-fill">
                            <div className="list-group" style={{ paddingBottom: "15px" }}>
                              <div className="card">
                                <div className="card-body">
                                  <div className="row">
                                    <img
                                      onClick={() => {
                                        setFirst_picture(picture);
                                      }}
                                      src={picture}
                                      alt={picture}
                                      style={{ width: "150px", margin: "auto", cursor:"pointer" }}
                                    />
                                  </div>
                                  {
                                    my_profile &&
                                    <div className="row">
                                        <button
                                          type="button"
                                          onClick={() => my_profile.delete_picture(picture)}
                                          //onClick={() => my_profile.delete_picture("http://localhost:3000/profile")}
                                          className="btn btn-danger btn-block"
                                          style={{ width: "150px", margin: "auto" }}
                                        >
                                          Supprimer
                                        </button>
                                    </div>
                                  }
                                </div>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                  <div className="col-sm-4 col-lg-4"> </div>
                </div>
                {
                  my_profile &&
                    <div>
                      <div className="row">
                        <label className="btn btn-success" style={{ width: "150px", margin: "auto" }} for="files">Ajouter une photo</label>
                      </div>
                      <input id="files" style={{visibility: "hidden"}} type="file"  onChange={(e) => {my_profile.send_picture(e.target.files[0])}}></input>
                    </div>
                }
                <br />
                {
                  detail && 
                <div className="row">
                  <div className="col-lg-3"></div>
                  <div className="col-lg-2" style={{ textAlign: "center" }}>
                    <button type="button" className="btn btn-warning">
                      Dénoncer un abus
                    </button>
                  </div>
                  <div className="col-lg-2" style={{ textAlign: "center" }}>
                    {(user[0].liked && (
                      <i
                        style={{ cursor: "pointer", color: "red" }}
                        onClick={() => {
                          detail.like_management(detail.match_id, false);
                          get_user();
                        }}
                        className="fa fa-heart fa-2x"
                      >
                        {" "}
                      </i>
                    )) || (
                      <i
                        style={{ cursor: "pointer", color: "red" }}
                        onClick={() => {
                          detail.like_management(detail.match_id, true);
                          get_user();
                        }}
                        className="far fa-heart fa-2x"
                      >
                        {" "}
                      </i>
                    )}
                  </div>
                  <div className="col-lg-2" style={{ textAlign: "center" }}>
                    <button onClick={() => detail.block_person(user[0].id, user[0].first_name + " " + user[0].lastname)} type="button" className="btn btn-danger">
                      Bloquer
                    </button>
                  </div>
                  <div className="col-lg-3"></div>
                </div>
                }
                <br />
                <div className="row">
                  <div className="col-lg-2">
                  </div>
                  <div className="col-lg-8">
                    <div className="card">
                      <h5
                        className="card-title"
                        style={{ textAlign: "center" }}
                      >
                        Tags
                      </h5>
                      <div className="card-body">
                        {
                          user[0].tags.map((val, i) => {
                          return (
                            <div key={i}>
                              <p>
                                {" "}{val}{" "}
                              </p>
                            </div>)
                          })
                        }
                        {
                          my_profile &&
                            <div className="input-group">
                              <input type="text" value={my_profile.newTag} onChange={(e) => my_profile.setNewTag(e.target.value)}  placeholder="Nouveau tag" className="form-control" aria-label="Text input with segmented dropdown button"/>
                              <div class="input-group-append">
                                <button type="button" className="btn btn-outline-secondary dropdown-toggle dropdown-toggle-split" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                  Suggestions{" "}
                                  <span className="sr-only">Toggle Dropdown</span>
                                </button>
                                <div className="dropdown-menu">
                                  {
                                    my_profile.suggestions[0] ?
                                    my_profile.suggestions.map( suggestion => {
                                    return <a style={{cursor:"pointer"}} onClick={(e) => my_profile.setNewTag(suggestion)} className="dropdown-item">{ suggestion }</a>
                                    })
                                    :
                                    <a className="dropdown-item">Aucun tag a affiché</a>
                                  }
                                </div>
                                <button type="button" onClick={() => my_profile.send_tags()} className="btn btn-success">Ajouter</button>
                              </div>
                            </div>
                        }
                      </div>
                    </div>
                  </div>
                  <div className="col-lg-2">
                  </div>
                </div>
                <br/>
                <div className="row">
                  <div className="col-sm-12 col-lg-6">
                    <div className="card">
                      <h5
                        className="card-title"
                        style={{ textAlign: "center" }}
                      >
                        Infos
                      </h5>
                      <div className="card-body">
                        <div className="row">
                          <div className="col-sm-6 col-lg-6">
                            <p>Age</p>
                          </div>
                          <div className="col-sm-6 col-lg-6">
                            {
                              detail ?
                              <p>{user[0].age}</p>
                              :
                              <input type="text" onChange={(e) => {my_profile.setAge(e.target.value);my_profile.setIsmodify(true)}} value={user[0].age}/>
                            }
                          </div>
                        </div>
                        <div className="row">
                          <div className="col-sm-6 col-lg-6">
                            <p>Sexe</p>
                          </div>
                          <div className="col-sm-6 col-lg-6">
                            {
                              detail ?
                              <p>{user[0].sex}</p>
                              :
                              <input type="text" onChange={(e) => {my_profile.setSex(e.target.value);my_profile.setIsmodify(true)}} value={user[0].sex}/>
                            }
                          </div>
                        </div>
                        {
                          detail &&
                          <div className="row">
                            <div className="col-sm-6 col-lg-6">
                              <p>Dernière connexion</p>
                            </div>
                            <div className="col-sm-6 col-lg-6">
                              <strong>{user[0].last_seen}</strong>
                            </div>
                          </div>
                        }
                      </div>
                    </div>
                  </div>
                  <div className="col-sm-12 col-lg-6">
                    <div className="card">
                      <h5
                        className="card-title"
                        style={{ textAlign: "center" }}
                      >
                        Description
                      </h5>
                      <div className="card-body">
                        {
                          detail ?
                          <p style={{ textAlign: "center" }}>{user[0].bio}</p>
                          :
                          <textarea className="form-control" onChange={(e) => {my_profile.setBio(e.target.value);my_profile.setIsmodify(true)}} value={user[0].bio}/>
                        }
                      </div>
                    </div>
                  </div>
                </div>
                <br />
                {
                  detail ?
                  <button
                    type="button"
                    onClick={() => history.push("/users")}
                    className="btn btn-danger btn-block"
                  >
                    Retour
                  </button>
                  :
                  
                  <div className="row">
                    <div className="col-sm-6 col-lg-6">
                      <button
                        type="button"
                        onClick={() => history.push("/users")}
                        className="btn btn-danger btn-block"
                      >
                        Retour
                      </button>
                    </div>
                    <div className="col-sm-6 col-lg-6">
                      <button
                        type="button"
                        onClick={() => my_profile.send_modification()}
                        className="btn btn-success btn-block"
                        disabled={my_profile.ismodify ? false : true}
                      >
                        Enregistrer
                      </button>
                    </div>
                  </div>
                }
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div
          style={{ lineHeight: "400px", height: "600px", textAlign: "center" }}
        >
          <Loader type="Hearts" color="red" height={200} width={200} />
          <p
            style={{
              position: "absolute",
              textAlign: "center",
              top: "150px",
              marginLeft: "auto",
              marginRight: "auto",
              left: "0",
              right: "0",
            }}
          >
            Chargement En cours ...
          </p>
        </div>
      )}
    </div>
  );
};

export default User_page;
