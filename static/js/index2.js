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
let choosecountpopup = document.body.querySelector('.choosecount');
let elemtsInitiallyHidden = document.body.querySelectorAll('[data-div = hidden]'); 
//let footer = document.body.querySelector('footer');

 
parameter.addEventListener("click", clickOnParameter);
parameters_options.addEventListener("click",clickOnParameterOptions);
newcount.addEventListener("click", choosenewcount);


/*Création à l'avance d'une popup en cas de click pour créer un tricount*/
/*let choosecountpopup = document.createElement('div');
choosecountpopup.className = "choosecount";
choosecountpopup.dataset.div = "hidden";
choosecountpopup.hidden = "hidden";

let countfromzero = document.createElement('a');
countfromzero.innerHTML = "Créer un nouveau tricount";
countfromzero.href = "/count/{{user}}/newcount"

let countfromclone = document.createElement('a'); 
countfromclone.innerHTML = "Clôner un tricount existant";


choosecountpopup.append(countfromzero);
choosecountpopup.append(countfromclone);*/

//ICI let elemtsInitiallyHidden = document.body.querySelectorAll('[data-div = hidden]'); 

//footer.append(choosecountpopup);

//OU ICI


/*Events handlers */
function clickOnParameter(event) { 
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

function choosenewcount(event){
    /*Fonction qui fait apparaître un choix sur la façon de créer le tricount*/
    toggle(choosecountpopup); 
    event.stopPropagation()
}