import React,{ FunctionComponent } from 'react';
import { Link } from 'react-router-dom'

const Navbar: FunctionComponent = () => {
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
                        <a href="#" className="nav-link">
                        <i className="fa fa-envelope"> </i>
                        <i className="fa fa-envelope-open"> </i>
                        </a>
                    </li>
                    <li className="nav-item">
                        <a href="#" className="nav-link">
                            <i className="fa fa-eye"> </i>
                            <i className="fa fa-eye-slash"> </i>
                            </a>
                    </li>
                    <li className="nav-item">
                        <a href="#" className="nav-link">
                            <i className="fa fa-bell"> </i>
                            <i className="fa fa-bell-slash"> </i>
                        </a>
                    </li>
                </ul>
            </div>
            <div className="navbar-collapse collapse w-100 order-3 dual-collapse2">
                <ul className="navbar-nav ml-auto">
                    <li className="nav-item">
                        <form className="form-inline" action="/action_page.php">
                            <input className="form-control mr-sm-2" type="text" placeholder="Search"/>
                            <button className="btn btn-danger" type="submit">Search</button>
                        </form>
                    </li>
                    <li className="nav-item dropdown">
                        <a href="#"
                            className="nav-link dropdown-toggle"
                            id="dropdown"
                            data-toggle="dropdown"
                        >
                            <i className="fa fa-user-circle"> </i>
                        </a>
                    </li>
                </ul>
            </div>
        </nav>
    )
}
const Navbar_tmp: FunctionComponent = () => {
    return (
<nav className="navbar navbar-expand-md navbar-dark bg-dark">
    <div className="navbar-collapse collapse w-100 order-1 order-md-0 dual-collapse2">
        <ul className="navbar-nav mr-auto">
            <li className="nav-item active">
                <a className="nav-link" href="#">Left</a>
            </li>
            <li className="nav-item">
                <a className="nav-link" href="//codeply.com">Codeply</a>
            </li>
            <li className="nav-item">
                <a className="nav-link" href="#">Link</a>
            </li>
            <li className="nav-item">
                <a className="nav-link" href="#">Link</a>
            </li>
            <li className="nav-item">
                <a className="nav-link" href="#">Link</a>
            </li>
        </ul>
    </div>
    <div className="mx-auto order-0">
        <a className="navbar-brand mx-auto" href="#">Navbar 2</a>
        <button className="navbar-toggler" type="button" data-toggle="collapse" data-target=".dual-collapse2">
            <span className="navbar-toggler-icon"></span>
        </button>
    </div>
    <div className="navbar-collapse collapse w-100 order-3 dual-collapse2">
        <ul className="navbar-nav ml-auto">
            <li className="nav-item">
                <a className="nav-link" href="#">Right</a>
            </li>
            <li className="nav-item">
                <a className="nav-link" href="#">Link</a>
            </li>
        </ul>
    </div>
</nav>
    )
}

export default Navbar;