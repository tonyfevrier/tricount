let username = document.querySelector('.username');
let email = document.querySelector('.email');
let password = document.querySelector('.password');
let submit = document.querySelector('.submit');

submit.addEventListener("click", blank);

let userlacking = document.createElement('p');
let emaillacking = document.createElement('p');
let pwdlacking = document.createElement('p');
userlacking.textContent = "A username is needed";
emaillacking.textContent = "An email is needed";
pwdlacking.textContent = "A password is needed";
userlacking.className = "userlacking";
emaillacking.className = "emaillacking";
pwdlacking.className = "pwdlacking";
userlacking.hidden = true;
emaillacking.hidden = true;
pwdlacking.hidden = true;
username.after(userlacking);
email.after(emaillacking);
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

    if (email.value.length == 0){
        event.preventDefault(); 
        emaillacking.hidden = false;
    } else {
        emaillacking.hidden = true;
    }

    if (password.value.length == 0){
        event.preventDefault(); 
        pwdlacking.hidden = false;
    } else {
        pwdlacking.hidden = true;
    }
}
 
 