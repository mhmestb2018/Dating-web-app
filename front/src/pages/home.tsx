import React, { FunctionComponent, useState } from 'react';
//import { useSelector, useDispatch } from 'react-redux';

type Props = {
    login: (email:String, password:String) => void;
    signup: (
        email:String,
        username:String,
        firstname:String,
        lastname:String
    ) => void;
};

const Home: FunctionComponent<Props> = ({login, signup}) => {
    //console.log(login);
    const [signinUsername, setSigninUsername] = useState('');
    const [signinPassword, setSigninPassword] = useState('');
    const [signupMail, setSignupMail] = useState('');
    const [signupUsername, setSignupUsername] = useState('');
    const [signupFirstname, setSignupFirstname] = useState('');
    const [signupLastname, setSignupLastname] = useState('');
    const [signupPassword, setSignupPassword] = useState('');
  return (
    <div>
        <br/>
        <div className="text-center row">
            <div className="col">
                <img src={process.env.PUBLIC_URL + '/asset/matcha.png'} width="60" height="60" alt="Matcha" className="d-inline-block align-top" style={{marginTop:-10}}/>
                <h1  className="d-inline-block align-top">atcha </h1>
            </div>
            <div className="col">
                <button type="button" className="btn btn-danger" data-toggle="modal" data-target="#modal_login">Connecte-toi !</button>
                <div className="modal fade" id="modal_login">
                    <div className="modal-dialog modal-dialog-centered modal-lg">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h4 className="modal-title">Connecte-toi !</h4>
                                <button type="button" className="close" data-dismiss="modal">&times;</button>
                            </div>
                            <div className="modal-body">
                                    <input onChange={(e) => setSigninUsername(e.target.value)} type="text" className="form-control" placeholder="Email" name="email"/>
                                    <br/>
                                    <input onChange={(e) => setSigninPassword(e.target.value)} type="password" className="form-control" placeholder="Mot de passe" name="password"/>
                                    <br/>
                            </div>
                            <div className="modal-footer">
                                <button onClick={() => login(signinUsername, signinPassword)} type="button" className="btn btn-success" data-dismiss="modal">Valider</button>
                            </div> 
                        </div>
                    </div>
                </div>
            </div>
            <br/>
        </div>
        <div className="text-center">
            <div id="homeCarousselFirst" className="carousel slide" data-ride="carousel">
                <ul className="carousel-indicators">
                    <li data-target="#homeCarousselFirst" data-slide-to="0" className="active"></li>
                    <li data-target="#homeCarousselFirst" data-slide-to="1"></li>
                    <li data-target="#homeCarousselFirst" data-slide-to="2"></li>
                    <li data-target="#homeCarousselFirst" data-slide-to="3"></li>
                </ul>
                <div className="carousel-inner">
                    <div className="carousel-item active">
                        <img src={process.env.PUBLIC_URL + '/asset/couple_1.jpg'} alt="Los Angeles" width="1100" height="500"/>
                        <div className="carousel-caption">
                            <h3>Le romantisme</h3>
                            <p>Invite la au restaurant</p>
                        </div>   
                    </div>
                    <div className="carousel-item">
                        <img src={process.env.PUBLIC_URL + '/asset/couple_2.jpg'} alt="Chicago" width="1100" height="500"/>
                        <div className="carousel-caption">
                            <h3>Sortie nature</h3>
                            <p>Rencontrez-vous à la plage</p>
                        </div>   
                    </div>
                    <div className="carousel-item">
                        <img src={process.env.PUBLIC_URL + '/asset/couple_3.jpg'} alt="New York" width="1100" height="500"/>
                        <div className="carousel-caption text-warning">
                            <h3>Sortie insolite</h3>
                            <p>Démarque toi et invite la à la patinoire</p>
                        </div>   
                    </div>
                    <div className="carousel-item">
                        <img src={process.env.PUBLIC_URL + '/asset/couple_disney.jpg'} alt="New York" width="1100" height="500"/>
                        <div className="carousel-caption">
                            <h3>Sortie stimulante</h3>
                            <p>Enmène la à Disney et fais lui revivre les bons souvenirs de son enfance</p>
                        </div>
                    </div>
                </div>
                <a className="carousel-control-prev" href="#homeCarousselFirst" data-slide="prev" style={{display: "none"}}>
                  <span className="carousel-control-prev-icon"><i className="fas fa-angle-double-left fa-5x" style={{color: 'red'}}></i></span>
                </a>
                <a className="carousel-control-next" href="#homeCarousselFirst" data-slide="next" style={{display: "none"}}>
                  <span className="carousel-control-next-icon"><i className="fas fa-angle-double-right fa-5x" style={{color: 'red'}}></i></span>
                </a>
            </div>
        </div>
        <br/>
        <div className="container">
            <button type="button" className="btn btn-danger btn-block"  data-toggle="modal" data-target="#modal_subscribe"> ➡ N'attend plus et inscris-toi ⬅</button>
            <div className="modal fade" id="modal_subscribe">
                <div className="modal-dialog modal-dialog-centered modal-lg">
                    <div className="modal-content">
                        <div className="modal-header">
                            <h4 className="modal-title">Inscription</h4>
                            <button type="button" className="close" data-dismiss="modal">&times;</button>
                        </div>
                        <div className="modal-body">
                            <form>
                                <div className="form-row">
                                    <div className="col">
                                        <input onChange={(e) => setSignupMail(e.target.value)} type="text" className="form-control" placeholder="Email" name="email"/>
                                    </div>
                                    <div className="col">
                                        <input onChange={(e) => setSignupUsername(e.target.value)} type="text" className="form-control" placeholder="Nom d'utilisateur" name="userName"/>
                                    </div>
                                </div>
                                <br/>
                                <div className="form-row">
                                    <div className="col">
                                        <input onChange={(e) => setSignupFirstname(e.target.value)} type="text" className="form-control" placeholder="Prénom" name="firstName"/>
                                    </div>
                                    <div className="col">
                                        <input onChange={(e) => setSignupLastname(e.target.value)} type="text" className="form-control" placeholder="Nom" name="lastName"/>
                                    </div>
                                </div>
                                <br/>
                                <div className="form-row">
                                    <div className="col">
                                        <input onChange={(e) => setSignupPassword(e.target.value)} type="text" className="form-control" placeholder="Mot de passe" name="firstPassword"/>
                                    </div>
                                    <div className="col">
                                        <input type="text" className="form-control" placeholder="Retapper le mot de passe" name="lastPassword"/>
                                    </div>
                                </div>
                            </form> 
                        </div>
                        <div className="modal-footer">
                            <button onClick={() => signup(signupMail, signupPassword, signupFirstname, signupLastname)} type="button" className="btn btn-success" data-dismiss="modal">Valider</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <br/>
        <div className="text-center row">
            <div className="col">
                <p>Finis les rencontres à l'autre bout du monde grâce à notre système de géolocalisation</p>
            </div>
            <div className="col">
                <p>Les meilleurs rencontres se font sur Matcha !</p>
            </div>
            <div className="col">
                <p>Notre algorithme choisit les matchs qui te correspondent vraiment afin que tu te désinscrive rapidement en ayant trouvé ton bonheur</p>
            </div>
            <br/>
        </div>
        <h2 className="text-center">
            Elles t'attendent
        </h2>
        <div className="row">
        <div className="col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                <div className="text-center">
                    <img src={process.env.PUBLIC_URL + '/asset/femme_1.jpg'} width="300" height="300" alt="Matcha_rose" className="d-inline-block align-top"/>
                </div>
            </div>
            <div className="col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                <div className="text-center">
                    <img src={process.env.PUBLIC_URL + '/asset/femme_2.jpg'} width="300" height="300" alt="Matcha_rose" className="d-inline-block align-top"/>
                </div>
            </div>
            <div className="col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                <div className="text-center">
                    <img src={process.env.PUBLIC_URL + '/asset/femme_3.jpg'} width="300" height="300" alt="Matcha_rose" className="d-inline-block align-top"/>
                </div>
            </div>
            <div className="col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                <div className="text-center">
                    <img src={process.env.PUBLIC_URL + '/asset/femme_4.jpg'} width="300" height="300" alt="Matcha_rose" className="d-inline-block align-top"/>
                </div>
            </div>
            <div className="col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                <div className="text-center">
                    <img src={process.env.PUBLIC_URL + '/asset/femme_5.jpg'} width="300" height="300" alt="Matcha_rose" className="d-inline-block align-top"/>
                </div>
            </div>
            <div className="col-12 col-sm-6 col-md-6 col-lg-4 col-xl-3">
                <div className="text-center">
                    <img src={process.env.PUBLIC_URL + '/asset/femme_6.png'} width="300" height="300" alt="Matcha_rose" className="d-inline-block align-top"/>
                </div>
            </div>
        </div>
    </div>
  );
}
  
export default Home;