// global variables
const creator = document.querySelector("input[name='nameparticipant']");
let number_ptcpt = 1; 
let compteur = document.createElement('p'); 
compteur.className = "compteur"; 
let list_participants = [document.body.querySelector('input[name = "nameparticipant"]').value];

window.addEventListener('DOMContentLoaded', (event) => {

    // Recover the currency if we come from currency pahe
    const params = new URLSearchParams(window.location.search); 

    if (window.location.search.includes("currency")){
        document.querySelector('.newtricount_currency').value = params.get('currency');
    }

    // Recover previous inputs if the user come from the currency page 
    recover_user_inputs(event);

    // Event to display letter counter when user clicks on a text input
    document.addEventListener("click", user_clicking);

    // Same when user writes in an input 
    document.addEventListener("input", user_writing);

    // Limit the length of a user text input
    let max_letters = 50;
    document.addEventListener("keydown", (event) => user_taping(event, max_letters));

    // Event to withdraw the creator of the tricount of the participants
    document.querySelector('.closeparticipant').addEventListener('click', (event) => user_closing_participant(event, creator.value));

    // Event to add participants to the tricount 
    document.querySelector('.add_participant').addEventListener("click", (event) => user_adding_participant(event, document.querySelector('.new_participant').value));

    // Event when clicking on currency
    document.querySelector('.choose-currency').addEventListener("click", click_on_currency);

    // Event when submitting the new tricount
    document.querySelector('.submittricount').addEventListener('click', submit_tricount);

})

function user_writing(event){  
    if (event.target.type !== 'text') return; 

    // Print the number of letters when the user writes something
    display_letter_counter(event);
}

function user_clicking(event){ 
    // Print the number of letters when the users clicks on an input
    if (event.target.type !== 'text') return; 
    display_letter_counter(event);
}

function user_taping(event, max_letters){ 
    if (event.target.type !== 'text') return; 

    // Limit the number of letters
    if (event.target.className === "newtricount_description"){
        max_letters = 500; 
    }
    if (event.target.value.length >= max_letters){ 
        if (event.key === "Backspace") return;
        else event.preventDefault();
        }
}

function display_letter_counter(event, max_letters){
    /*Function which add a counter behind the input*/

    //Choice of the maximal number of letters
    if (event.target.className === "newtricount_description") {max_letters = 500;}
    else {max_letters = 50;}
    
    // Create the letter counter
    compteur.innerHTML = `<p> ${event.target.value.length}/${max_letters} </p>`;

    //Introduction of the element at the good place in the html
    if (event.target.className === "new_participant"){ 
        document.querySelector(".add_participant").after(compteur);
    } else {
        event.target.after(compteur);
    } 
} 


function user_adding_participant(event, name){
    /*Function which adds html elements when user adds a participant*/ 

    // Do nothing if the user writes nothing 
    if (name === 'Autre participant' || name === '') return;

    // Do nothing if the participant is already included 
    if (list_participants.includes(name)){
        document.querySelector('.new_participant').value = '';
        return;
    } 

    // Create a participant
    let printparticipant = document.createElement('div');
    printparticipant.className = "printparticipant";
    printparticipant.innerHTML = `<input class = "nameparticipant" type="text" value = "${name}" name = "nameparticipant"><button class = "closeparticipant" name = "${name}" ><img src="/static/images/close.png" alt="fermeture"></button>`;
    document.querySelector('.participants-container').append(printparticipant); 
    document.querySelector('.newtricount').insertAdjacentHTML('beforeend',`<input type="text" class="formparticipant" value = "${name}" name = "formparticipant" hidden>`); 

    // Update the participants counter and add him to participants list 
    number_ptcpt += 1;
    document.querySelector('.nb_participants').innerHTML = `Participants (${number_ptcpt}/50)`;
    list_participants.push(name);
    document.querySelector('.new_participant').value = ''; 

    //Creation of event for closing the new participant 
    closeparticipant = document.querySelector(`.closeparticipant[name=${name}]`); 
    closeparticipant.addEventListener("click", (event) => user_closing_participant(event, name)); 
}

function user_closing_participant(event, name){ 

    event.target.closest('.printparticipant').remove(); 
    document.querySelector(`.formparticipant[value=${name}]`).remove();

    // Update
    number_ptcpt -= 1;
    const index = list_participants.indexOf(name);
    list_participants.splice(index, 1);
    document.querySelector('.nb_participants').innerHTML = `Participants (${number_ptcpt}/50)`;
}

function click_on_currency(event){
    /*Function to keep what the user's inputs in local storage before he chooses the currency */

    event.preventDefault();
    localStorage.clear();

    // Put inputs in memory
    localStorage.setItem("titre", document.querySelector('.newtricount_title').value);
    localStorage.setItem("description", document.querySelector('.newtricount_description').value); 

    const category = document.querySelector('.newtricount_category:checked'); 
    if (category) localStorage.setItem("category", category.value); 

    for (let participant of document.querySelectorAll('.nameparticipant')){
        localStorage.setItem(`${participant.value}`, participant.value);
    }

    // Go to the page of currencies to choose one
    window.location.href = document.querySelector('.choose-currency').getAttribute("href");
}

function recover_user_inputs(event){
    /* Function to recover what has been to put in local storage if we come from the currency page */
    if (!document.referrer.includes('currency')) return;

    document.querySelector('.newtricount_title').value = localStorage.getItem("titre");
    document.querySelector('.newtricount_description').value = localStorage.getItem("description"); 
  
    // Check the category if stored
    category = localStorage.getItem("category"); 
    if (category){ 
        document.querySelector(`[value = ${category}]`).checked = true; 
    }

    // Get stored participants
    is_creator_in_participants = false;
    for (let i = 0; i < localStorage.length; i++){
        if (!["titre","description","category"].includes(localStorage.key(i))){
            //document.querySelector('.new_participant').value = localStorage.getItem(localStorage.key(i));
            user_adding_participant(event, localStorage.getItem(localStorage.key(i)));

            if (localStorage.key(i) === creator.value) is_creator_in_participants = true 
        }
    }

    // Delete the creator if it was not in list of participants (views automatically put it)
    if (!is_creator_in_participants){ 
        document.querySelectorAll(".printparticipant")[0].remove();
        const index = list_participants.indexOf(creator.value);
        list_participants.splice(index, 1);
        number_ptcpt -= 1;
        document.querySelector('.nb_participants').innerHTML = `Participants (${number_ptcpt}/50)`;
    }
}

function submit_tricount(event){
    // Get inputs filled by the user
    const title = document.querySelector('.newtricount_title');
    const password = document.querySelector('.newtricount_pwd');
    const category = document.querySelector('.newtricount_category:checked');
    const participants = document.querySelectorAll('.nameparticipant');
  
    // Submit tricount if inputs are present
    if (title.value && password.value && category && participants.length >= 2) return;

    // Hide eventual showed messages
    document.querySelector("#title-error").hidden = true;
    document.querySelector("#pwd-error").hidden = true;
    document.querySelector("#category-error").hidden = true;
    document.querySelector("#participant-error").hidden = true;

    // Do not submit and write error messages if it lacks inputs
    event.preventDefault();  
    if (!title.value) {document.querySelector("#title-error").hidden = false;}  
    if (!password.value) {document.querySelector("#pwd-error").hidden = false;}  
    if (!category) {document.querySelector("#category-error").hidden = false;}  
    if (participants.length < 2) {document.querySelector("#participant-error").hidden = false;}
    
}