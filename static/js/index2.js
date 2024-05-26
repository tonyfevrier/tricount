/*
Essayer de ne mettre qu'un événement sur le doc et d'assigner des méthodes différentes suivant là où on clique.
    click sur l'engrenage : apparition d'un élément 
    click sur bas : apparition d'un élément
    click sur qqch qui n'est ni un lien ni un cadre ouvert : réinitialisation de la page initiale.
    clic sur un lien de l'élément généré par l'engrenage : un autre élément remplace le précédent.
*/

document.addEventListener("click", goback);

let parameter = document.querySelector('.parameters');  
let parameters_options = document.querySelector('.parameters-options'); 
let newcount = document.body.querySelector('.id_newcount');
let clonecount = document.body.querySelector('.clonecount');
let choosecountpopup = document.body.querySelector('.choosecount');
let pwdcountpopup = document.body.querySelector('.form-pwdcount');
let form = pwdcountpopup.firstElementChild; 
let pwdinput = form.firstElementChild; 
let pwdsubmit = form.lastElementChild;
let error = document.createElement("div");
error.dataset.div = "hidden";
error.className = "error";
error.innerHTML = "Entrez un mot de passe";
error.hidden = true;
form.append(error);
let elemtsInitiallyHidden = document.body.querySelectorAll('[data-div = hidden]'); 
 
parameter.addEventListener("click", clickOnParameter);
parameters_options.addEventListener("click",clickOnParameterOptions);
newcount.addEventListener("click", clickOnNewcount);
choosecountpopup.addEventListener("click", clickOnChooseCount);
pwdsubmit.addEventListener("click", clickOnSubmit);




/*Events handlers */
function clickOnParameter(event) { 
    if (isOnePopUpApparent()) return;
    if (event.currentTarget == parameter){ 
        toggle(parameters_options);  
        display_block_for_children(parameters_options)
        event.stopPropagation(); //éviter que le listener goback soit lancé
    }
}

function clickOnParameterOptions(event){
    if (!event.target.dataset.button) return;
    /*on récupère la classe de l'élément JS
    on fait apparaître l'élément dont le nom est le nom de la classe -options.
    on cache parameter options*/
    const classname = event.target.className;
    toggle(parameters_options);  
    const child = document.body.querySelector(`.${classname}-options`)
    toggle(child);
    display_block_for_children(child);
    event.stopPropagation();
}

function goback(event){ 
    // si aucune popup n'est apparente, on garde le comportement initial de la page.
    if (!isOnePopUpApparent()) return;
    //si on ne clique pas sur une div ayant l'attribut data-div, on retourne à la page pop up ouverte.
    if (!event.target.closest('div')?.dataset.div){ 
        event.preventDefault(); //désactiver les liens.
        hide();
    }
}


/*Utilities */
function toggle(elem){
    elem.hidden = !elem.hidden;
}

function isOnePopUpApparent(){
    let bool = false;
    for (elem of elemtsInitiallyHidden){ 
        if (elem.hidden === false){ 
            bool = true;
        }
    }  
    return bool;
}

function hide(){
    //on récupère tous les éléments ayant un data-div = hidden et on les cache.
    for (elem of elemtsInitiallyHidden) elem.hidden = true;
}

function display_block_for_children(elem){
    for (let child of elem.children){
        child.style.display = "block";
    }
}

function clickOnNewcount(event){
    /*Fonction qui fait apparaître un choix sur la façon de créer le tricount*/
    if (isOnePopUpApparent()) return;
    if (pwdcountpopup.hidden === false) return;
    choosecountpopup.hidden = false;
    event.stopPropagation();
}

function clickOnChooseCount(event){
    /*Fonction qui ouvre la popup demandant le mot de passe du tricount à clôner*/ 
    // Si on clique sur autre chose que clonecount onretourne 
    // sinon je cache idnewcount, et je rends visible le form, et j'empêche la propag au clic du document

    if (event.target != clonecount) return;
    choosecountpopup.hidden = true;
    pwdcountpopup.hidden = false;  
    event.stopPropagation();
}

function clickOnSubmit(event){
    /*Fonction qui traite le cas où l'utilisateur oublie de mettre un mot de passe. Apparition d'un message d'erreur */
    /*Si on clique et que le input est vide */
    if (pwdinput.value !== "submit password" && pwdinput.value !== "") return;
    event.preventDefault();
    error.hidden = false;  
}