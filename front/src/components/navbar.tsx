import React,{ FunctionComponent } from 'react';
import { Link } from 'react-router-dom'

type Props = {
    logout: () => void;
};

const Navbar: FunctionComponent<Props> = ({logout}) => {
    return (
        <nav className="navbar sticky-top navbar-expand-md navbar-dark bg-dark">
            <Link to="/" className="navbar-brand">
                <img src={process.env.PUBLIC_URL + '/asset/matcha.png'} width="30" height="30" alt="Matcha" className="d-inline-block align-top"/>atcha
            </Link>
            <button type="button" className="navbar-toggler" data-toggle="collapse" data-target="#navbar">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbar">
                <ul className="navbar-nav mr-auto">
                    <li className="nav-item active">
                        <a href="/mailbox" className="nav-link">
                        <i className="fa fa-envelope"> </i>
                        {/*<i className="fa fa-envelope-open"> </i>*/}
                        </a>
                    </li>
                    <li className="nav-item">
                        <a href="#" className="nav-link">
                            <i className="fa fa-eye"> </i>
                            {/*<i className="fa fa-eye-slash"> </i>*/}
                            </a>
                    </li>
                    <li className="nav-item">
                        <a href="#" className="nav-link">
                            <i className="fa fa-bell"> </i>
                            {/*<i className="fa fa-bell-slash"> </i>*/}
                        </a>
                    </li>
                </ul>
            </div>
            <div className="navbar-collapse collapse w-100 order-3 dual-collapse2">
                <ul className="navbar-nav ml-auto">
                    <li className="nav-item dropdown">
                        <a className="nav-link dropdown-toggle" id="navbarDropdownMenuLink-4" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><i className="fa fa-newspaper-o"></i> 
                        <i className="fa fa-user-circle"> </i> </a>
                        <div className="dropdown-menu dropdown-menu-right dropdown-cyan" aria-labelledby="navbarDropdownMenuLink-4">
                            <a className="dropdown-item" href="/my_profile">Mon profil</a>
                            <a className="dropdown-item" href="/my_account">Mon compte</a>
                            <a className="dropdown-item" style={{backgroundColor:"#ff0000", color:"white", cursor: "pointer"}} onClick={() => logout()}>Se déconnecter</a>
                        </div>
                    </li>
                </ul>
            </div>
        </nav>
    )
}

export default Navbar;