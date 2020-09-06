/* eslint-disable */
import React,{ FunctionComponent, useState } from 'react';
import Navbar from './components/navbar'
import Footer from './components/footer'
import UserList from './pages/user-list'
import UserDetail from './pages/user-detail'
import Home from './pages/home'
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom'

import PageNotFound from './pages/page-not-found'

import axios from 'axios';

const App: FunctionComponent = () => {
    const login = (email:String, password:String) => {alert(email);setIsLogged(true);}
    const [IsLogged, setIsLogged] = useState<Boolean>(false);
    /*axios.post(`app:5000/login`, { 'email':'gdssgs', 'password':'sgsssg' })
    .then(res => {
        alert('123');
        console.log(res);
        console.log(res.data);
    })*/

    return (
        <Router>
                <Navbar />
                <Switch>
                    <Route exact path="/" component={() => !IsLogged&&<Home login={login}/>||<UserList/>}/>
                    <Route exact path="/users" component={IsLogged&&UserList||Home}/>
                    <Route path="/users/:id" component={IsLogged&&UserDetail||Home}/>
                    <Route component={PageNotFound}/>
                </Switch>
                <Footer/>
                
        </Router>
    )
}

export default App;
//https://www.udemy.com/course/reactjs-tutorial-francais-authentication-api-rest-autocomplete-router/learn/lecture/17374676#overview