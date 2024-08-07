let maxLetters = 50;
let listparticipants = [document.body.querySelector('input[name = "nameparticipant"]').value];
 
let compteur = document.createElement('p'); 
compteur.className = "compteur"; 
const textInputs = document.body.querySelectorAll("input[type = 'text']");
const addparticipant = document.body.querySelector('.add_participant');
const new_participant = document.body.querySelector('.new_participant');
const form = document.body.querySelector('.newtricount');  
const nb_participants = document.body.querySelector('.nb_participants');
let number_ptcpt = 1;

// Events carrying on inputs of type text.
document.addEventListener("input", userWriting);
document.addEventListener("click", userClicking);
document.addEventListener("keydown", userTaping);
addparticipant.addEventListener("click", userAddingParticipant);

//Récupération de la monnaie dans l'url si on vient de la liste des monnaies.
const url = window.location.search; 
const params = new URLSearchParams(url);
let currency = document.querySelector('.newtricount_currency');

if (url.includes("currency")){
    currency.value = params.get('currency');
}

//Stocker puis récupérer les données préécrites lors du chargement de page
let formulaire = document.querySelector('form')
const link_to_currency = document.querySelector('.choose-currency');
link_to_currency.addEventListener("click", currencyClicking);

document.addEventListener('DOMContentLoaded',recoverItems)

function userWriting(event){ 
    //Afficher le compteur quand le nombre de lettres change.
    if (event.target.type !== 'text') return; 

    //On affiche le compteur
    displayCounter(event);
     
}

function userClicking(event){ 
    //Afficher le compteur dès qu'on clique sur l'input
    if (event.target.type !== 'text') return; 
    displayCounter(event);
    
}

function userTaping(event){
    //Limiter le nombre de lettres à 50 ou 500.
    if (event.target.type !== 'text') return; 
    if (event.target.className === "newtricount_description"){
        maxLetters = 500; 
    }
    if (event.target.value.length >= maxLetters){ 
        if (event.key === "Backspace") return;
        else event.preventDefault();
        }
}

function displayCounter(event){
    /*Function which add a counter behind the input*/
    
    //Introduction of the element at the good place in the html
    if (event.target.className === "new_participant"){ 
        document.body.querySelector(".add_participant").after(compteur);
    } else {
        event.target.after(compteur);
    } 

    //Choice of the innerHTML depending on the input.
    if (event.target.className === "newtricount_description"){
        maxLetters = 500;
    }   else {
        maxLetters = 50;
    }
    compteur.innerHTML = `<p> ${event.target.value.length}/${maxLetters} </p>`;
} 
 
function userAddingParticipant(event){
    /*Function which adds html elements when user adds a participant*/
    
    if (new_participant.value === 'Autre participant' || new_participant.value === '') return;
 
    if (listparticipants.includes(new_participant.value)){
        new_participant.value = '';
        return;
    } 

    //Creation of a participant
    let printparticipant = document.createElement('div');
    printparticipant.className = "printparticipant";
    printparticipant.innerHTML = `<input class = "nameparticipant" type="text" value = "${new_participant.value}" name = "nameparticipant"><button class = "closeparticipant" name = "${new_participant.value}" ><img src="/static/images/close.png" alt="fermeture"></button>`;

    form.append(printparticipant); 

    //Mise à jour de différentes valeurs. 
    number_ptcpt += 1;
    nb_participants.innerHTML = `Participants (${number_ptcpt}/50)`;
    listparticipants.push(new_participant.value);
    new_participant.value = ''; 

    //Creation of event for closing the participants
    closeparticipants = document.body.querySelectorAll('.closeparticipant');
    for (let closeparticipant of closeparticipants){
        closeparticipant.addEventListener("click", userClosingParticipant);
    }   
}

function userClosingParticipant(event){
    /*Function which removes html element of a participant */ 
    event.target.closest('.printparticipant').remove();

    //Mise à jour
    number_ptcpt -= 1;
    nb_participants.innerHTML = `Participants (${number_ptcpt}/50)`;

}


function currencyClicking(event){
    /*Function to put what the user writes in local storage */

    event.preventDefault();

    localStorage.clear();
    //récupérer les données de description titre, category et participants
    localStorage.setItem("titre", formulaire.newtricount_title.value);
    localStorage.setItem("description", formulaire.newtricount_description.value); 

    let category = document.body.querySelector('.newtricount_category:checked'); 
    if (category) localStorage.setItem("category", category.value); 

    let participants = formulaire.querySelectorAll('.nameparticipant');
    for (let participant of participants){
        localStorage.setItem(`${participant.value}`, participant.value);
    }
    

    //remettre le comportement par défaut
    window.location.href = link_to_currency.getAttribute("href");
}

function recoverItems(event){
    /*Function to recover what has been to put in local storage if we come from the currency page*/
    if (!document.referrer.includes('currency')) return;

    formulaire.newtricount_title.value = localStorage.getItem("titre");
    formulaire.newtricount_description.value = localStorage.getItem("description"); 
 
    console.log(localStorage);
    //si on une valeur dans newtricount_category, on checked la case correspondante.
    category = localStorage.getItem("category"); 
    if (category){ 
        formulaire.querySelector(`[value = ${category}]`).checked = true; 
    }

    for (let i = 0; i < localStorage.length; i++){
        let key = localStorage.key(i);
        if (!["titre","description","category"].includes(key)){
            new_participant.value = localStorage.getItem(key);
            userAddingParticipant();
        }
    }
     
}