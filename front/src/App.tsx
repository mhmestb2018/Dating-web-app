/* eslint-disable */
import React,{ FunctionComponent } from 'react';
import Navbar from './components/navbar'
import Footer from './components/footer'
import UserList from './pages/user-list'
import UserDetail from './pages/user-detail'
import Home from './pages/home'
import { BrowserRouter as Router, Switch, Route, Link } from 'react-router-dom'

import PageNotFound from './pages/page-not-found'

const App: FunctionComponent = () => {

    return (
        <Router>
            <div>
                <Navbar/>
                <Switch>
                    <Route exact path="/" component={Home}/>
                    <Route exact path="/users" component={UserList}/>
                    <Route path="/users/:id" component={UserDetail}/>
                    <Route component={PageNotFound}/>
                </Switch>
                <Footer/>
            </div>
        </Router>
    )
}

export default App;
//https://www.udemy.com/course/reactjs-tutorial-francais-authentication-api-rest-autocomplete-router/learn/lecture/17374676#overview