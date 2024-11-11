let receivers = document.querySelectorAll(".receiver");
let click = new Event("click", {bubbles: true,});

window.addEventListener('DOMContentLoaded', (event) => {

    // Change the currency if the user has chosen an other currency.
    const url = window.location.search;
    const params = new URLSearchParams(url);    

    if (url.includes("currency")){
        document.querySelector('.newtricount_currency').value = params.get('currency');
    }   

    // Recover previous inputs if the user come from the currency page 
    recover_user_inputs(event);

    for (let monnaie of document.querySelectorAll('.p-currency')){ 
        monnaie.innerHTML = document.querySelector('.newtricount_currency').value;
    }

    // Display the number of letters of title
    document.querySelector(".title").addEventListener("input", user_writing);

    // Event on keyboard to limit the number of letters
    document.querySelector(".title").addEventListener("keydown", user_taping);

    // Event to share an amount automatically to checked people
    document.querySelector(".amount").addEventListener("input", user_amount);

    // Event when clicking on currency
    document.querySelector('.choose-currency').addEventListener("click", click_on_currency);

    // Event to handle the check/uncheck of participants
    document.querySelector(".list-receivers").addEventListener("click", user_checking);

    // Event to handle the global check of participants
    document.querySelector(".toggle-checkboxes").addEventListener("click",user_toggle);

    // Event for the user clicking on "Avancé" to personalize more the share of a spending
    document.querySelector('.special-parameters').addEventListener("click", user_avance); 

    // Event to prevent spending submit if some inputs are empty
    document.querySelector('.submit-spending').addEventListener('click', submit_spending);

    // Handle the modifyspending page option to delete the spending 
    if (document.querySelector("footer").innerText){
        document.querySelector(".delete-spending").addEventListener("click",
             () => user_delete_spending(document.querySelector('.tricount').id, document.querySelector('.header-title').id));
    }
})


/*Handlers */
function user_writing(){ 
    // Display the counter when the number of letters change 
    document.querySelector(".counter").innerHTML = `${document.querySelector(".title").value.length}/50`;
}

function user_taping(event){
    /* Prevent the user from taping too much letters. */
    if (event.target.value.length >= 50){
        if (event.key == "Backspace") return;
        else event.preventDefault();
    } 
}

function user_amount(){
    // When user writes an amount, it is shared among checked people 
    const table = calculate_individual_amounts_and_store_spending_participants_with_parts(); 
    attribute_individual_amount_with_parts(table[0],table[1],table[2]); 
}


function user_checking(event){ 
    /* Clic on a checkbox, participant is checked or unchecked */
    if (event.target.type !== 'checkbox') return; 
    // compute the amounts each person must pay after a modification 
    user_amount(); 

    // If someone is unchecked, we uncheck the global checkbox
    if (!event.target.checked) document.querySelector(".toggle-checkboxes").checked = false;
}


function user_toggle(){ 
    /* Check all users if one user was unchecked, otherwise uncheck everybody*/
    const nb_checked = number_of_checked_people();
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

function user_avance(event){
    /* Handle the advanced share of the spending */
    insert_or_remove_parts_for_spending(document.querySelector('.special-parameters').innerHTML);
    event.preventDefault();
}

function user_delete_spending(id_count, id_spending){
    /* Handle to delete a spending*/
    const confirmation = confirm("Do you want to delete this spending")
    if (confirmation) {window.location.href = `/deletespending/${id_count}/${id_spending}`;}
    return;
} 

function submit_spending(event){
    // Get inputs filled by the user
    const title = document.querySelector('.title'); 
    const participants = document.querySelectorAll('.receiver:checked'); 
  
    // Submit spending if inputs are present
    if (title.value && participants.length) return;

    // Hide eventual showed messages
    document.querySelector("#title-error").hidden = true; 
    document.querySelector("#participant-error").hidden = true;

    // Do not submit and write error messages if it lacks inputs
    event.preventDefault();  
    if (!title.value) {document.querySelector("#title-error").hidden = false;}   
    if (!participants.length) {document.querySelector("#participant-error").hidden = false;}
}


function click_on_currency(event){
    /*Function to keep what the user's inputs in local storage before he chooses the currency */

    event.preventDefault();
    localStorage.clear();

    // Put inputs in memory
    localStorage.setItem("titre", document.querySelector('.title').value);
    localStorage.setItem("amount", document.querySelector('.amount').value); 
    localStorage.setItem("spender", document.querySelector('.spender').value); 

    // Go to the page of currencies to choose one
    window.location.href = document.querySelector('.choose-currency').getAttribute("href");
}

function recover_user_inputs(event){
    /* Function to recover what has been to put in local storage if we come from the currency page */
    if (!document.referrer.includes('currency')) return;

    // Get stored data
    document.querySelector('.title').value = localStorage.getItem("titre");
    document.querySelector('.amount').value = localStorage.getItem("amount"); 
    document.querySelector('.spender').value = localStorage.getItem("spender"); 

    // Share the amount among checked users
    if (document.querySelector('.amount').value) user_amount();
}




/*Useful functions for handlers*/

function calculate_individual_amounts_and_store_spending_participants_with_parts(event){
    let list_of_checked = [];
    let list_of_non_checked = [];

    /* See how many checks there are to compute the number of parts */
    let nb_parts = 0;
    for (let receiver of receivers){ 
        if (receiver.checked){
            // See if parts are displayed 
            if (document.querySelector(`.${receiver.id}-parts`)) {
                nb_parts += Number(document.querySelector(`.${receiver.id}-parts`).value);
            } else {
                nb_parts += 1;
            }
            list_of_checked.push(receiver.id);
        } else {
            list_of_non_checked.push(receiver.id);
        }
    }

    // Get the amount by person  
    let individual_amount_dico = {};

    for (let checkman of list_of_checked){
        let poids = 1;
        if (document.querySelector(`.${checkman}-parts`)) { 
            poids =  Number(document.querySelector(`.${checkman}-parts`).value); 
        } 
        individual_amount_dico[checkman] = amount.value * poids/nb_parts;
    } 

    return [individual_amount_dico, list_of_checked,list_of_non_checked];
}
 
function attribute_individual_amount_with_parts(individual_amount_dico, list_of_checked,list_of_non_checked){
    
    for (let checked_receiver of list_of_checked){  
        document.querySelector(`.${checked_receiver}-amount`).value = `${individual_amount_dico[checked_receiver].toFixed(2)}`;

    }
    for (let non_checked_receiver of list_of_non_checked){ 
        document.querySelector(`.${non_checked_receiver}-amount`).value = `0.00`;
    }
}



function number_of_checked_people(){
    let nb_checked = 0; 
    for (let receiver of receivers){
        if (receiver.checked){
            nb_checked += 1; 
        }  
    } 
    return nb_checked;
}

function insert_or_remove_parts_for_spending(innerHTML){
    /*Si on clique sur avancé, on fait apparaître les parts de chacun et l'utilisateur peut modifier le nombre de parts, ce qui recalcule les montants*/
    if (innerHTML === "Advanced"){ 
        document.querySelector('.special-parameters').innerHTML = "Simple"; 
        for (let receiver of receivers){
            montant = document.querySelector(`.${receiver.id}-amount`); 
            if (receiver.checked){
                montant.insertAdjacentHTML("beforebegin",`<input type = "text" class = "${receiver.id}-parts" value = "1" >`); 
            } else {  
                montant.insertAdjacentHTML("beforebegin",`<input type = "text" class = "${receiver.id}-parts" value = "0">`); 
            }
            document.querySelector(`.${receiver.id}-parts`).addEventListener("input",user_amount);
        }
    } else { 
         document.querySelector('.special-parameters').innerHTML = "Advanced";
        for (let receiver of receivers){
            document.querySelector(`.${receiver.id}-parts`).removeEventListener("input",user_amount);
            document.querySelector(`.${receiver.id}-parts`).remove();
        } 
        user_amount()
    }
}

