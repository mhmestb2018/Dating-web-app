import React, { FunctionComponent, useState, useEffect } from "react";
import { textChangeRangeIsUnchanged } from "typescript";


import Map from 'pigeon-maps'
import Marker from 'pigeon-marker'
import Overlay from 'pigeon-overlay'
const MyAccount = () => {
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
                    <div className="col-lg-4">address@email.com</div>
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
                  <div className="row">
                    <div className="col-lg-6">Pierre</div>
                    <div className="col-lg-6" style={{textAlign:"center"}}>
                      <button type="button" className="btn btn-success">
                        Débloquer
                      </button>
                    </div>
                  </div>
                  <br />
                  <div className="row">
                    <div className="col-lg-6">Marie</div>
                    <div className="col-lg-6" style={{textAlign:"center"}}>
                      <button type="button" className="btn btn-success">
                        Débloquer
                      </button>
                    </div>
                  </div>
                  <br />
                  <div className="row">
                    <div className="col-lg-6">Diego</div>
                    <div className="col-lg-6" style={{textAlign:"center"}}>
                      <button type="button" className="btn btn-success">
                        Débloquer
                      </button>
                    </div>
                  </div>
                  <br />
                  <div className="row">
                    <div className="col-lg-6">Madonna</div>
                    <div className="col-lg-6" style={{textAlign:"center"}}>
                      <button type="button" className="btn btn-success">
                        Débloquer
                      </button>
                    </div>
                  </div>
                  <br />
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
                            <Map center={["45.75", "4.85"]} zoom={12} width={600} height={400}>
                                <Marker anchor={["45.75", "4.85"]} payload={1} onClick={({ event, anchor, payload }) => {}} />
                                <Overlay anchor={["45.75", "4.85"]} offset={[120, 79]}>
                                <img src='https://cdn.intra.42.fr/users/medium_pcachin.jpg' width={24} height={15} alt='' />
                                </Overlay>
                            </Map>
                            <br/>
                            <br/>
                            <br/>
                            <button type="button" className="btn btn-success">
                                Modifier ma position
                            </button>
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