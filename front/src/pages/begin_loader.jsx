import React, { FunctionComponent, useState } from 'react';
//import { useSelector, useDispatch } from 'react-redux';

import Loader from 'react-loader-spinner'
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css"
const Begin_loader = () => {
  return (
    <div style={{lineHeight: "400px", height: "600px", textAlign: "center"}}>
      <Loader type="Hearts" color="red" height={200} width={200} />
      <p style={{position: "absolute", textAlign: "center", top: "150px", marginLeft: "auto", marginRight: "auto", left: "0", right: "0"}}>Chargement En cours ...</p>
    </div>
  );
}
  
export default Begin_loader;