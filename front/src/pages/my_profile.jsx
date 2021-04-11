import React, { FunctionComponent, useState, useEffect } from 'react';
import User from '../models/user';

import User_page from "./user_page"
//import formatDate from '../helpers/format-date'

import { useHistory } from 'react-router-dom'

import Loader from 'react-loader-spinner'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"

import axios from 'axios';


const MyProfile = ({toast}) => {

  useEffect(() => {
    get_user()
}, [])

  const get_user = () => {
    setLoader(true)
    axios.get('/profile')
    .then(res => {
        setFirst_name(res.data.first_name);
        setLast_name(res.data.last_name);
        setAge(parseInt(res.data.age));
        setBio(res.data.bio);
        setSex(res.data.sex);
        setPictures(res.data.pictures);
        alert(res.data.pictures);
        setTags(res.data.tags);
        setIsmodify(false);
        console.log(res)
    })
    .catch(function (error) {
        console.log(error)
        alert("error_get_users");
    })
    axios.get('/tags')
    .then(res => {
      setSuggestions(res.data.tags);
        console.log(res)
    })
    .catch(function (error) {
        console.log(error)
        alert("error_get_tags");
    })
    setLoader(false);
  }

const [loader, setLoader] = useState(true);

const [first_name, setFirst_name] = useState("");
const [last_name, setLast_name] = useState("");
const [age, setAge] = useState(0);
const [bio, setBio] = useState("");
const [sex, setSex] = useState("");
const [pictures, setPictures] = useState([]);
const [tags, setTags] = useState([]);
const [ismodify, setIsmodify] = useState(false);
const [suggestions, setSuggestions] = useState([]);
const [newTag, setNewTag] = useState("");



const send_picture = (picture) => {
  var bodyFormData = new FormData();
  bodyFormData.append('file', picture); 
  axios({
    method: 'post',
    url: '/add_picture',
    data: bodyFormData,
    headers: {'Content-Type': 'multipart/form-data' }
    })
  .then(res => {
      console.log(res);
      console.log(res.data);
      toast.success("Votre nouvelle photo a été enregistré avec succés !");
      setPictures(res.data.pictures);
  })
  .catch(function (error) {
        // console.log(error.response.data);
        // console.log(error.response.status);
        console.log(error);
      toast.error(error);
    });
}
const delete_picture = (picture) => {
  alert(`DEL: ${picture}`);
  console.log(picture)
  axios({
    method: 'delete',
    url: picture,
    headers: {'Content-Type': 'multipart/form-data' }
    })
  .then(res => {
      console.log(res);
      console.log(res.data);
      toast.success("Votre nouvelle photo a été supprimé avec succés !");
      setPictures(res.data.pictures);
  })
  .catch(error => {
        // console.log(error.response.data);
        // console.log(error.response.status);
        //console.log(error);
      toast.error("error");
    });
}

  const send_modification = () => {
    setLoader(true);
    axios.put("/profile",
    {
      'first_name':first_name,
      'last_name':last_name,
      "age": age,
      "bio":bio,
      "sex":sex,
    })
    .then((res) => {
      setFirst_name(res.data.first_name);
      setLast_name(res.data.last_name);
      setAge(parseInt(res.data.age));
      setBio(res.data.bio);
      setSex(res.data.sex);
      setPictures(res.data.pictures);
      setTags(res.data.tags);
      setIsmodify(false);
    })
    .catch(function (error) {
      get_user()
    });
    setLoader(false);
  }

  const send_tags = () => {
    setLoader(true);
    axios.put("/profile",
    {
      "tags": [...tags, newTag]
    })
    .then((res) => {
      setTags([...tags, newTag])
    })
    .catch(function (error) {
      alert("ERROR")
    });
    setLoader(false);
  }

  return (
    <div>
      <User_page user={[{first_name, last_name, age, bio, sex, pictures, tags}]} detail={false} my_profile={{send_tags, setNewTag, newTag, suggestions, delete_picture, send_picture, setFirst_name, setLast_name, setAge, setBio, setSex, setPictures, setTags, send_modification, ismodify, setIsmodify}} loader={loader} get_user={get_user}/>
    </div>
  );
}

export default MyProfile;