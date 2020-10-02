/* eslint-disable */
import React,{ FunctionComponent, useState, useEffect } from 'react';
import User from '../models/user';
import USER_LIST from '../models/mock-user';
import UserCard from '../components/user-card'
import getGenderColor from '../helpers/get-gender-color'


const UserList: FunctionComponent = () => {
    const [users, setUSers] = useState<User[]>([]);

    useEffect(() => {
        setUSers(USER_LIST);
    },[])//Le [] veut dire que l on execute setUSers seulement si pokemons vaut [] (la premiere fois seulement quoi ^^)

    return (
        <div>
            <p>Il y à {users ? users.length : 0} utilisateurs sur le site</p>
            <div className="container-fluid">
                <div className="row">
                    <div className="col-sm-3 col-2 border">
                        <p>Les plus populaires</p>
                        <p>Les plus populaires</p>
                        <p>Les plus populaires</p>
                        <p>Les plus populaires</p>
                        <p>Les plus populaires</p>
                    </div>
                    <div className="col-sm-9 col-10">
                        <div className="row">
                        {users && users.map((user) => (
                            <UserCard user={user} key={user.id} borderColorHover={getGenderColor(user.gender)}/>
                        ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default UserList;