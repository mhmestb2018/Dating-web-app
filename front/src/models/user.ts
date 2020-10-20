export default class User {
    // 1. Typage des propiétés d'un user.
    age: number;
    blocked: boolean;
    first_name: string;
    last_name: string;
    id: number;
    last_seen: string;
    liked: boolean;
    matches: boolean;
    pictures: Array<string>;
    sex: string;
    bio: string;

    // 2. Définition des valeurs par défaut des propriétés d'un user.
    constructor(
        age: number,
        blocked: boolean,
        first_name: string,
        last_name: string,
        id: number,
        last_seen: string,
        liked: boolean,
        matches: boolean,
        pictures: Array<string>,
        sex: string,
        bio: string,
    ) {
     // 3. Initialisation des propiétés d'un user.
     this.age = age;
     this.blocked = blocked;
     this.first_name = first_name;
     this.last_name = last_name;
     this.id = id;
     this.last_seen = last_seen;
     this.liked = liked;
     this.matches = matches;
     this.pictures = pictures;
     this.sex = sex;
     this.bio = bio;
    }
}