const formatDate = (gender:string):string => {//Recupere la date (au format Date) dans un format correct à afficher
    return gender === "Female" ? "pink" : gender === "Male" ? "blue" : "purple"
}

export default formatDate;