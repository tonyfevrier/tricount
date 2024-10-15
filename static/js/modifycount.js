let errormessage = document.createElement("div");
errormessage.className = "error";
errormessage.innerHTML = "Veuillez remplir le champ";
errormessage.hidden = true;

window.addEventListener("DOMContentLoaded", () => {
    // Create the hidden error message when adding a blank participant
    document.querySelector('.add_participant').after(errormessage);

    // Event to delete participants
    document.querySelector('.participants-container').addEventListener("click", user_closing_participant);

    // Event to add participants
    document.querySelector('.add_participant').addEventListener("click",user_adding_participant);

    // Event to delete tricount
    document.querySelector("footer").addEventListener("click", () => user_delete_tricount(document.querySelector('.titre').id)); 

    // Submit the tricount modified or block it if information lacks
    document.querySelector('.submittricount').addEventListener('click', submit_tricount);
})


function user_closing_participant(event){
    /*Function which removes from the tricount the participant closed by the admin*/
    event.preventDefault();   
    if (event.target.tagName != "IMG" && event.target.tagName != "BUTTON") return;
    event.target.closest(".printparticipant").remove();
}

function user_adding_participant(event){
    /*Function which adds the participant written in the associated input or write an error message if the input field isn't filled.*/
    let inputparticipant = document.body.querySelector('.new_participant');

    // Display an error if no value, create a participant otherwise
    if (!inputparticipant.value){
        errormessage.hidden = false;
    } else {
        document.querySelector('.participants-container').insertAdjacentHTML("beforeend",`
                <div class = "printparticipant">
                    <input class = "nameparticipant" type="text" value = "${inputparticipant.value}" name = "nameparticipant">
                    <button class = "closeparticipant" name = "{{participant}}" ><img src="/static/images/close.png" alt="fermeture"></button>
                </div>`);
        inputparticipant.value = "";
        errormessage.hidden = true;
    }
}

function user_delete_tricount(id){
    /*Function to manage the delation of the tricount*/  
    const confirmation = confirm('Do you confirm deleting the count?')
    if (confirmation){
        window.location.href = `/deletecount/${id}`
    }
    return;
}


function submit_tricount(event){
    // Get inputs filled by the user
    const title = document.querySelector('.tricount_title');
    const description = document.querySelector('.tricount_description'); 
    const participants = document.querySelectorAll('.nameparticipant');
  
    // Submit tricount if inputs are present
    if (title.value && description.value && participants.length >= 2) return;

    // Hide eventual showed messages
    document.querySelector("#title-error").hidden = true;
    document.querySelector("#description-error").hidden = true; 
    document.querySelector("#participant-error").hidden = true;

    // Do not submit and write error messages if it lacks inputs
    event.preventDefault();  
    if (!title.value) {document.querySelector("#title-error").hidden = false;}  
    if (!description.value) {document.querySelector("#description-error").hidden = false;}   
    if (participants.length < 2) {document.querySelector("#participant-error").hidden = false;}   
}