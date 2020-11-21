const formatDate = (gender:string):string => {//Recupere la date (au format Date) dans un format correct à afficher
    return gender === "female" ? "pink" : gender === "male" ? "blue" : "purple"
}

export default formatDate;