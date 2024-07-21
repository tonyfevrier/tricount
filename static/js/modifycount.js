/*TODO
clic sur je suis : apparition d'un check input pour choisir le propriétaire et disparition du ajouter
 */

let errormessage = document.createElement("div");
errormessage.innerHTML = "Veuillez remplir le champ";
errormessage.hidden = true;

let participants = document.body.querySelector('.participants-container');
let addparticipant = document.body.querySelector('.add_participant');
let inputparticipant = document.body.querySelector('.new_participant');
const footer = document.body.querySelector("footer");
const deletebutton = footer.firstElementChild;
const deletealert = footer.lastElementChild;
addparticipant.after(errormessage);

window.addEventListener("click", alertBlockScreen);
participants.addEventListener("click", userClosingParticipant);
addparticipant.addEventListener("click",userAddingParticipant);
footer.addEventListener("click", userDeleteTricount); 

function userClosingParticipant(event){
    /*Function which removes from the tricount the participant closed by the admin*/
    event.preventDefault();   
    if (event.target.tagName != "IMG" && event.target.tagName != "BUTTON") return;
    event.target.closest(".printparticipant").remove();
}

function userAddingParticipant(event){
    /*Function which adds the participant written in the associated input or write an error message if the input field isn't filled.*/
    if (!inputparticipant.value){
        errormessage.hidden = false;
    } else {
        participants.insertAdjacentHTML("beforeend",`
                <div class = "printparticipant">
                    <input class = "nameparticipant" type="text" value = "${inputparticipant.value}" name = "nameparticipant">
                    <button class = "closeparticipant" name = "{{participant}}" ><img src="/static/images/close.png" alt="fermeture"></button>
                </div>`);
        inputparticipant.value = "";
        errormessage.hidden = true;
    }
}

function userDeleteTricount(event){
    /*Function to manage the delation of the tricount*/ 
   if (event.target === deletebutton){
        deletealert.hidden = false;
   } else if (event.target === deletealert.lastElementChild){
        deletealert.hidden = true;
   } 
   return;
}

function alertBlockScreen(event){
    /*Function which prevents from clicking on another button if the alert of delation of tricount has appeared */
    if (deletealert.hidden === false && event.target.className != "yesno" ){
        event.preventDefault()
    }
    return;
}