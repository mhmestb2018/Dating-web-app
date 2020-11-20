import React, { FunctionComponent, useState, useEffect } from "react";
import User from "../models/user";
//import formatDate from '../helpers/format-date'

import { useHistory } from "react-router-dom";
import User_page from "./user_page"

import axios from "axios";
import { useRouteMatch } from "react-router-dom";

const UsersDetail = ({ like_management, toast }) => {
  let match_id = useRouteMatch("/users/:id").params.id;
  const history = useHistory();

  const [user, setUser] = useState([]);
  const [first_picture, setFirst_picture] = useState("");


  const block_person = (user_id, name) => {
    axios.post('/users/' + user_id,
    {
      "block" : true
    })
    .then(res => {
        console.log(res);
        console.log(res.data);
        toast.success("Vous avez bien blocké " + name + " :)");
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

  const get_user = () => {
    setLoader(true);
    axios
      .get(`/users/${match_id}`)
      .then((res) => {
        setUser(Array(res.data));
        setFirst_picture(res.data.pictures[0]);
      })
      .catch(function (error) {
        console.log(error);
        alert("error_get_users");
        //setIsLoad(true);
      });
    setLoader(false);
  };
  useEffect(() => {
    get_user();
  }, []);

  const [loader, setLoader] = useState(true);

  return (
    <div>
      <User_page user={user} my_profile={false} loader={loader} detail={{match_id, like_management, block_person}} get_user={get_user}/>
    </div>
  );
};

export default UsersDetail;
