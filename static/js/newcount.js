let maxLetters = 50;
 
let compteur = document.createElement('p'); 
compteur.className = "compteur"; 
const textInputs = document.body.querySelectorAll("input[type = 'text']");
const addparticipant = document.body.querySelector('.add_participant');
const new_participant = document.body.querySelector('.new_participant');
const form = document.body.querySelector('.newtricount');  
const nb_participants = document.body.querySelector('.nb_participants');
let number_ptcpt = 0;

// Events carrying on inputs of type text.
document.addEventListener("input", userWriting);
document.addEventListener("click", userClicking);
document.addEventListener("keydown", userTaping);
addparticipant.addEventListener("click", userAddingParticipant);


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
    
    if (new_participant.value === 'Autre participant') return;

    //Creation of a participant
    let printparticipant = document.createElement('div');
    printparticipant.className = "printparticipant";
    printparticipant.innerHTML = `<input class = "nameparticipant" type="text" value = "${new_participant.value}" name = "nameparticipant">
    <button class = "closeparticipant"><img src="{%static 'images/close.png'%}" alt="fermeture"></button>`;
    form.append(printparticipant); 

    //Mise à jour de différentes valeurs.
    new_participant.value = '';  
    number_ptcpt += 1;
    nb_participants.innerHTML = `Participants (${number_ptcpt}/50)`;

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