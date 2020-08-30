const formatDate = (date:Date):string => {//Recupere la date (au format Date) dans un format correct à afficher
    return `${date.getDate()}/${date.getMonth()+1}/${date.getFullYear()}`
}

export default formatDate;