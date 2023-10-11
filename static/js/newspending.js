/*
input sur le titre : compteur sur le nb de lettres           ok
montant rempli : calcul automatique de la part de chacune des personnes cochées. 
clic sur checkbox de pour qui : coche ou décoche tous
clic sur avancé : apparition de parts pour chaque participant et du mot simple à la place de "avancé"
    changement des parts : recalcul des montants de chaque personne cochée.
clic sur simple : disparition des parts et apparition de avancé.
clic sur dépense : élément avec choix. 
clic sur eur : élement avec Eur et plus
*/

const title = document.body.querySelector("[placeholder = 'Titre']");
const amount = document.body.querySelector(".amount");
let counter = document.body.querySelector(".counter");
let checkboxDiv = document.body.querySelector(".list-receivers");  
let receivers = document.body.querySelectorAll(".receiver");


title.addEventListener("input", userWriting);
title.addEventListener("keydown", userTaping);
amount.addEventListener("input", userAmount);
checkboxDiv.addEventListener("click",userChecking);


function userWriting(event){ 
    //Afficher le compteur quand le nombre de lettres change. 
    counter.innerHTML = `${title.value.length}/50`;
}

function userTaping(event){
    /*si on a trop de caractères dans le titre. */
    if (event.target.value.length >= 50){
        if (event.key == "Backspace") return;
        else event.preventDefault();
    } 
}

function userAmount(event){
    //Quand l'utilisateur écrit un montant, il est partagé sur les personnes cochées.
    
    let table = calculateIndividualAmountsAndStoreSpendingParticipants(event); 
    attributeIndividualAmount(table[0],table[1]);
}


function userChecking(event){
    //Clic sur une checkbox : le participant est décoché ou coché 
    if (event.target.type !== 'checkbox') return; 
    //si on coche quelqu'un, on recalcule la répartition des montants. 
    userAmount(event);

    
    /*if (event.target.checked){ 
        console.log(1);
    } else {
        console.log(2);
    }*/
}

function calculateIndividualAmountsAndStoreSpendingParticipants(event){
    /*on compte le nb de personnes cochées et on les listes*/
    let list_of_checked = [];
    let nb_checked = 0;
    for (let receiver of receivers){
        if (receiver.checked){
            nb_checked += 1;
            list_of_checked.push(receiver.id);
        } 
    }

    /*on calcule le montant par personne*/
    let individualAmount = event.target.value/nb_checked; 
    return [individualAmount, list_of_checked];
}

function attributeIndividualAmount(individualAmount, list_of_checked){
    for (let checked_receiver of list_of_checked){
        document.body.querySelector(`.${checked_receiver}-amount`).innerHTML = `${individualAmount} eur`;
    }
}
