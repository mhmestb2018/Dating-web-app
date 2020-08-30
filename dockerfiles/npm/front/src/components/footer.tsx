import React, { FunctionComponent } from 'react';
import { useHistory } from 'react-router-dom'
  
const Footer: FunctionComponent = () => {
    const history = useHistory()

    const goToAccueil = () => {
        history.push('/')
    }

  return (
        <footer className="page-footer font-small teal pt-4">
            <div style={{backgroundColor:"#D3D3D3"}}>
            <div className="container-fluid text-center text-md-left">
                <hr className="mt-3 mb-3"/>
                <div className="row">
                    <div className="col-md-6 mt-md-0 mt-3  text-center">
                        <h5 className="text-uppercase font-weight-bold">Guillaume Madec</h5>
                        <p>Réalisation de la partie front-end en javascript avec React.js et bootstrap4</p>
                        <ul className="list-unstyled list-inline text-center">
                            <li className="list-inline-item">
                                <a className="btn-floating btn-fb mx-1">
                                    <i className="fab fa-facebook"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-tw mx-1">
                                    <i className="fab fa-twitter"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-gplus mx-1">
                                    <i className="fab fa-google-plus-g"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-li mx-1">
                                    <i className="fab fa-linkedin-in"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-dribbble mx-1">
                                    <i className="fab fa-dribbble"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-dribbble mx-1">
                                    <i className="fab fa-github"></i>
                                </a>
                            </li>
                        </ul>
                    </div>
                    <hr className="clearfix w-100 d-md-none pb-3"/>
                    <div className="col-md-6 mt-md-0 mt-3  text-center">
                        <h5 className="text-uppercase font-weight-bold">Phillipe Cachin</h5>
                        <p>Réalisation de la partie back-end et base de donnée en python avec flask et Mysql</p>
                        <ul className="list-unstyled list-inline text-center">
                            <li className="list-inline-item">
                                <a className="btn-floating btn-fb mx-1">
                                    <i className="fab fa-facebook"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-tw mx-1">
                                    <i className="fab fa-twitter"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-gplus mx-1">
                                    <i className="fab fa-google-plus-g"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-li mx-1">
                                    <i className="fab fa-linkedin-in"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-dribbble mx-1">
                                    <i className="fab fa-dribbble"> </i>
                                </a>
                            </li>
                            <li className="list-inline-item">
                                <a className="btn-floating btn-dribbble mx-1">
                                    <i className="fab fa-github"></i>
                                </a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <hr/>
            <div className="footer-copyright text-center py-3">
                © 2020 Copyright: Matcha
            </div>
            </div>
        </footer>
  );
}
  
export default Footer;