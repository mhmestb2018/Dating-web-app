export default class User {
    // 1. Typage des propiétés d'un pokémon.
    id: number;
    name: string;
    picture: string;
    types: Array<string>;
    created: Date;
    gender:string;
     
    // 2. Définition des valeurs par défaut des propriétés d'un pokémon.
    constructor(
     id: number,
     name: string = 'name',
     picture: string = 'http://...',
     types: Array<string> = ['Normal'],
     created: Date = new Date(),
     gender:string = 'Unknow',
    ) {
     // 3. Initialisation des propiétés d'un pokémons.
     this.id = id;
     this.name = name;
     this.picture = picture;
     this.types = types;
     this.created = created;
     this.gender = gender;
    }
   }