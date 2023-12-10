let username = document.querySelector('.username'); 
let password = document.querySelector('.password');
let submit = document.querySelector('.submit');

submit.addEventListener("click", blank);

let userlacking = document.createElement('p'); 
let pwdlacking = document.createElement('p');
userlacking.textContent = "A username is needed"; 
pwdlacking.textContent = "A password is needed";
userlacking.className = "userlacking"; 
pwdlacking.className = "pwdlacking";
userlacking.hidden = true; 
pwdlacking.hidden = true;
username.after(userlacking); 
password.after(pwdlacking);

 
function blank(event){
    /*function which prevents the form to be sent if the user has not entered username or email or password.
    It also add an element telling the lack of username/email/password*/
    
    if (username.value.length == 0){
        event.preventDefault(); 
        userlacking.hidden = false;
    } else {
        userlacking.hidden = true;
    }

    if (password.value.length == 0){
        event.preventDefault(); 
        pwdlacking.hidden = false;
    } else {
        pwdlacking.hidden = true;
    }
}
 
 