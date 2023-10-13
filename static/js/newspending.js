/*
clic sur avancé : apparition de parts pour chaque participant et du mot simple à la place de "avancé"
    changement des parts : recalcul des montants de chaque personne cochée. 
clic sur dépense : élément avec choix. 
clic sur eur : élement avec Eur et plus
*/

const title = document.body.querySelector("[placeholder = 'Titre']");
const amount = document.body.querySelector(".amount");
let counter = document.body.querySelector(".counter");
let checkboxDiv = document.body.querySelector(".list-receivers");  
let receivers = document.body.querySelectorAll(".receiver");
let toggleCheckbox = document.body.querySelector(".toggle-checkboxes");
let toggleAvance = document.body.querySelector('.special-parameters'); 


title.addEventListener("input", userWriting);
title.addEventListener("keydown", userTaping);
amount.addEventListener("input", userAmount);
checkboxDiv.addEventListener("click",userChecking);
toggleCheckbox.addEventListener("click",userToggle);
toggleAvance.addEventListener("click", userAvance);


let click = new Event("click", {bubbles: true,});



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

function userAmount(){
    //Quand l'utilisateur écrit un montant, il est partagé sur les personnes cochées.
    let table = calculateIndividualAmountsAndStoreSpendingParticipants(); 
    attributeIndividualAmount(table[0],table[1],table[2]); 
}


function userChecking(event){ 
    //Clic sur une checkbox : le participant est décoché ou coché 
    if (event.target.type !== 'checkbox') return; 
    //si on coche quelqu'un, on recalcule la répartition des montants. 
    userAmount(); 

    //si on décoche un participant, on décoche le checkbox principal */
    if (!event.target.checked) toggleCheckbox.checked = false;
}

function userToggle(event){ 
    /*dans le cas où au moins 1 n'était pas coché, tout le monde devient coché.*/
    nb_checked = NumberOfCheckedPeople();
    if (nb_checked < receivers.length){
        for (let receiver of receivers){ 
            receiver.checked = true;
            receiver.dispatchEvent(click);
        }
    } else {
        for (let receiver of receivers){ 
            receiver.checked = false;
            receiver.dispatchEvent(click);
        }
    }
}

function userAvance(event){
    /*apparition/disparition de nouveau hidden + chgt en simple ou avancé */
    insertOrRemovePartsForSpending(toggleAvance.innerHTML);
    event.preventDefault();
}



function calculateIndividualAmountsAndStoreSpendingParticipants(){
    /*on compte le nb de personnes cochées et on les liste*/
    let list_of_checked = [];
    let list_of_non_checked = [];
    let nb_checked = 0;
    for (let receiver of receivers){
        if (receiver.checked){
            nb_checked += 1;
            list_of_checked.push(receiver.id);
        } else {
            list_of_non_checked.push(receiver.id);
        }
    }

    /*on calcule le montant par personne*/
    //let individualAmount = event.target.value/nb_checked; 
    let individualAmount = amount.value/nb_checked; 
    return [individualAmount, list_of_checked,list_of_non_checked];
}

function attributeIndividualAmount(individualAmount, list_of_checked,list_of_non_checked){
    for (let checked_receiver of list_of_checked){
        document.body.querySelector(`.${checked_receiver}-amount`).innerHTML = `${individualAmount.toFixed(2)} eur`;
    }
    for (let non_checked_receiver of list_of_non_checked){
        document.body.querySelector(`.${non_checked_receiver}-amount`).innerHTML = `0.00 eur`;
    }
}

function NumberOfCheckedPeople(){
    let nb_checked = 0; 
    for (let receiver of receivers){
        if (receiver.checked){
            nb_checked += 1; 
        }  
    } 
    return nb_checked;
}

function insertOrRemovePartsForSpending(innerHTML){
    /*Si on clique sur avancé, on fait apparaître les parts de chacun et l'utilisateur peut modifier le nombre de parts, ce qui recalcule les montants*/
    if (innerHTML === "Avancé"){ 
        toggleAvance.innerHTML = "Simple"; 
        for (let receiver of receivers){
            montant = document.body.querySelector(`.${receiver.id}-amount`); 
            if (receiver.checked){
                montant.insertAdjacentHTML("afterbegin",`<input type = "text" class = "${receiver.id}-parts" value = "1" >`); 
            } else {  
                montant.insertAdjacentHTML("afterbegin",`<input type = "text" class = "${receiver.id}-parts" value = "0">`); 
            }
            document.body.querySelector(`.${receiver.id}-parts`).addEventListener("input",userAmountParts);
        }
    } else {
        toggleAvance.innerHTML = "Avancé";
        for (let receiver of receivers){
            document.body.querySelector(`.${receiver.id}-parts`).remove();
        }
    }
    
}

function userAmountParts(event){
    /* */
    console.log(5);
    //userAmount();
}
