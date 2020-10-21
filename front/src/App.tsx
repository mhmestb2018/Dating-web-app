/* eslint-disable */
import React,{ FunctionComponent, useState } from 'react';
import Navbar from './components/navbar'
import Footer from './components/footer'
import UserList from './pages/user-list'
import UserDetail from './pages/user-detail'
import MyProfile from './pages/my_profile'
import Begin_loader from './pages/begin_loader'
import Chat_widget from './pages/chat_widget'
import Home from './pages/home'
import Mailbox from './pages/mailbox'
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom'

import My_account from './pages/my_account'

import PageNotFound from './pages/page-not-found'

import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { JSDocUnknownType } from 'typescript';


const App: FunctionComponent = () => {
    const login = (email:String, password:String) => {
      //alert("SEND")
        axios.post('/login',
          {
            'email':email,
            'password':password,
            "remember_me": false
          }
        )
        //axios.get('/debug')
        .then(res => {

        setIsLogged(true);
            //alert('123');
            console.log(res);
            console.log(res.data);
            toast.success("Vous êtes connécté :)");
        })
        .catch(function (error) {
              // console.log(error.response.data);
              // console.log(error.response.status);
              console.log(error);
              if (error.response.data)
                toast.error(error.response.data.error);
              else
                toast.error("Erreur de connection avec le serveur");
          });
    }

    const forget_password = (email:String) => {
      //alert("SEND")
        axios.post('/reset',
          {
            'email':email
          }
        )
        //axios.get('/debug')
        .then(res => {

        setIsLogged(true);
            //alert('123');
            console.log(res);
            console.log(res.data);
            var new_password = window.prompt('Nouveau password ?');
            

        axios.post('/reset/<user_id>/<reset_id>',
        {
          'new_password':new_password
        }
        )
            toast.success("ReSeT PaSsWoRd :)");
        })
        .catch(function (error) {
              // console.log(error.response.data);
              // console.log(error.response.status);
              console.log(error);
              if (error.response.data)
                toast.error(error.response.data.error);
              else
                toast.error("Erreur de connection avec le serveur");
          });
    }

    const logout = () => {
        axios.post('/logout')
        .then(res => {
          setIsLogged(false);
            console.log(res);
            console.log(res.data);
            toast.success("Vous êtes bien déconnécté :)");
        })
        .catch(function (error) {
              // console.log(error.response.data);
              // console.log(error.response.status);
              console.log(error);
              if (error.response.data)
                toast.error(error.response.data.error);
              else
                toast.error("Erreur de connection avec le serveur");
          });
    }
    const signup = (email:String, password:String, firstname:String, lastname:String) => {
      //axios.post('http://app:5000/login', { 'email':'gdssgs', 'password':'sgsssg' })
      axios.post('/signup',
        {
           'email':email,
           //'username':username,
           "password":password,
           "first_name":firstname,
           "last_name":lastname 
        }
      )
      .then(res => {
        console.log(res);
        alert("SUCCESS_signup");
        axios.post('/validate/' + res.data.validation_id,
      )
      .then(res => {
        console.log(res);
        alert("SUCCESS_validate");
      })
      .catch(function (error) {
            console.log(error);
            alert("ERROR_validate");
        });
      })
      .catch(function (error) {
            console.log(error);
            alert("ERROR_signup");
        });
  }

  const like_management = (user_id : String, like: Boolean) => {
    axios.post('/users/' + user_id,
    {
      "like" : like
    })
    .then(res => {
        console.log(res);
        console.log(res.data);
        if (like)
          toast.success("Vous avez bien liké :)");
        else
          toast.success("Vous avez bien enlevé le like :)");
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

    const [IsLogged, setIsLogged] = useState<Boolean>(false);
    const [IsLoad, setIsLoad] = useState<Boolean>(false);

      axios.get('/profile')
      .then(res => {
        setIsLogged(true);
        setIsLoad(true);
      })
      .catch(function (error) {
        setIsLoad(true);
        });
    return (
        <Router>
          <ToastContainer
          position="top-center"
          autoClose={5000}
          hideProgressBar={false}
          newestOnTop={false}
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          />
          {IsLogged && <Navbar logout={logout} />}
          {IsLoad &&
            <div>
                <Switch>
                    <Route exact path="/" component={() => !IsLogged&&<Home login={login} forget_password={forget_password} signup={signup}/>||<UserList/>}/>
                    <Route exact path="/my_profile" component={() => IsLogged && <MyProfile toast={toast} /> || <Home login={login} signup={signup} forget_password={forget_password}/>}/>
                    <Route exact path="/users" component={() => IsLogged && <UserList/> || <Home login={login} signup={signup} forget_password={forget_password} />}/>
                    <Route path="/users/:id" component={() => IsLogged && <UserDetail like_management={like_management}  toast={toast}/> || <Home login={login} signup={signup} forget_password={forget_password} /> }/>
                    <Route exact path="/mailbox" component={() => IsLogged && <Mailbox /> || <Home login={login} signup={signup} forget_password={forget_password}/>}/>
                    <Route exact path="/my_account" component={() => IsLogged && <My_account toast={toast}/> || <Home login={login} signup={signup} forget_password={forget_password}/>}/>
                    <Route component={PageNotFound}/>
                </Switch>
                {IsLogged && <Chat_widget />}
                <Footer/>
            </div>
            ||
            <Begin_loader />
          }
        </Router>
    )
}

export default App;
//https://www.udemy.com/course/reactjs-tutorial-francais-authentication-api-rest-autocomplete-router/learn/lecture/17374676#overview