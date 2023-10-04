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
let elemtsInitiallyHidden = document.body.querySelectorAll('[data-div = hidden]');
 
parameter.addEventListener("click", parameters);

/*Events handlers */
function parameters(event) { 
    if (event.currentTarget == parameter){ 
        toggle(parameters_options);  
        display_block_for_children(parameters_options)
        event.stopPropagation(); //éviter que le listener goback soit lancé
    }
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