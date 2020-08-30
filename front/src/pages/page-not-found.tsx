import React, { FunctionComponent } from 'react';
import { useHistory } from 'react-router-dom'
  
const PageNotFound: FunctionComponent = () => {
    const history = useHistory()

    const goToAccueil = () => {
        history.push('/')
    }

  return (
    <div className="text-center">
        <h1>Hey, cette page n'existe pas !</h1>
        <h1><img src={process.env.PUBLIC_URL + '/asset/matcha.png'} width="30" height="30" alt="Matcha" className="d-inline-block align-top"/>atcha</h1>
        <button onClick={()=> goToAccueil()} type="button" className="btn btn-primary">Retourner à l'accueil</button>
    </div>
  );
}
  
export default PageNotFound;