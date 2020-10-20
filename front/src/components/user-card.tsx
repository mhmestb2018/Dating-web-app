import React, { FunctionComponent, useState  } from "react";
import User from '../models/user'
import  './user-card.css'
import { useHistory } from 'react-router-dom'
type Props = {
    user: User,
    borderColorHover?: string
}
//Le ? veut dire que c est facultatif
const UserCard: FunctionComponent<Props> = ({user, borderColorHover='red'}) => {
    const [color, setColor] = useState<string>(borderColorHover);

    const history = useHistory()

    const showBorder = () => {
        setColor('red')
    }
    const hideBorder = () => {
        setColor(borderColorHover)
    }

    const goToUser = (id:number) => {
        history.push(`/users/${id}`)
    }

    return (
        <div className="col-sm-6 col-md-4 col-lg-3 col-xl-2">
            <div onClick={() => goToUser(user.id)} className="card horizontal shadow"  onMouseEnter={showBorder} onMouseLeave={hideBorder} style={{borderColor:color, cursor: "pointer"}}>
                <img className="card-img-top" src={user.pictures[0]} alt={user.pictures[0]}  width="400" height="200"/>
                <div className="card-body">
                    <h4 className="card-title text-center">{user.first_name}</h4>
                    {/*<p className="card-text">{created.toString()}</p>*/}
                    {<p className="card-text">{user.sex}</p>}
                    {/*user.types.map(type => (
                        <span key={type} className="badge badge-pill badge-secondary">{type}</span>
                    ))*/}
                </div>
            </div>
            <br/>
        </div>
    )
}

export default UserCard;