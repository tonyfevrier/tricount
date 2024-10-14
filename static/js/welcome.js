window.addEventListener('DOMContentLoaded', () =>{ 
    document.querySelector('.submit').addEventListener("click", (event) => tell_lack_input(event));
})

function tell_lack_input(event){
    /* Prevents the form to be sent if the user has not entered username or email or password. */

    // Remove existing messages
    const printed_errors = document.querySelectorAll('.lack'); 
        for (error of printed_errors){error.remove();}
    
    // Create error messages if one input is empty
    if (document.querySelector('.username').value.length == 0){
        event.preventDefault(); 
        create_error_element("A username is needed", document.querySelector('.username')) 
    } 
    
    if (document.querySelector('.email') && document.querySelector('.email').style.display != 'none' && document.querySelector('.email').value.length == 0){
        event.preventDefault(); 
        create_error_element("An email is needed", document.querySelector('.email')) 
    } 

    if (document.querySelector('.password').value.length == 0){
        event.preventDefault(); 
        create_error_element("A password is needed", document.querySelector('.password')) 
    } 
}


function create_error_element(text, parent){  
    const userlacking = document.createElement('p');
    userlacking.textContent = text;
    userlacking.className = "lack"; 
    parent.after(userlacking);  
}
 