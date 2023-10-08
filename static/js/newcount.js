let maxLetters = 50;
let compteur = document.createElement('p'); 
compteur.className = "compteur"; 
const textInputs = document.body.querySelectorAll("input[type = 'text']");

// Events carrying on inputs of type text.
document.addEventListener("input", userWriting);
document.addEventListener("click", userClicking);
document.addEventListener("keydown", userTaping);


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
        document.body.querySelector(".addparticipant").append(compteur);
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
 