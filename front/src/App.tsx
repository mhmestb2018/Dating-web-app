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
    const __login = (email:String, password:String) => {
        //axios.post('http://app:5000/login', { 'email':'gdssgs', 'password':'sgsssg' })
        axios.get('/debug')
        //axios.post('http://app:5000/')
        //axios.get('https://randomuser.me/api/')
        .then(res => {
            alert('123');
            console.log(res);
            console.log(res.data);
        })
        .catch(function (error) {
              // console.log(error.response.data);
              // console.log(error.response.status);
              console.log(error);
              alert("ERROR");
          });

    /*      fetch('http://app:5000/profile', {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    firstParam: 'yourValue',
    secondParam: 'yourOtherValue',
  })
})*/

        //setIsLogged(true);
    }
    const [IsLogged, setIsLogged] = useState<Boolean>(false);

    return (
        <Router>
                <Navbar />
                <Switch>
                    <Route exact path="/" component={() => !IsLogged&&<Home login={__login}/>||<UserList/>}/>
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