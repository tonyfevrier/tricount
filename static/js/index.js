/*
Essayer de ne mettre qu'un événement sur le doc et d'assigner des méthodes différentes suivant là où on clique.
    click sur l'engrenage : apparition d'un élément 
    click sur bas : apparition d'un élément
    click sur qqch qui n'est ni un lien ni un cadre ouvert : réinitialisation de la page initiale.
    clic sur un lien de l'élément généré par l'engrenage : un autre élément remplace le précédent.
*/

document.addEventListener("click", parameters);

let parameters = document.querySelector('.parameters'); 
let parameters_options = document.querySelector('.parameters-options');
let create_tricount = document.querySelector('.create-tricount');
let help_options = document.querySelector('.help-options');

let help = document.querySelector('.help');
let conditions = document.querySelector('.conditions');



//IMPORTANT : Il faudrait une fonction click on button qui marche qqs la popup ouverte, qui prendrait une popup en argument
//en gros la même qui marche quand je clique sur l'engrenage devrait aussi marcher quand je clique sur le bouton d'une 
//popup ouverte. PCq là j'essaie d'imbriquer un événement dans un autre alors que moralement ça correpsond à deux événements analogues
//La question : comment coder une succession de clics sur des événements apparus entre temps en évitant une ribambelle de if imbriqués.
//Une idée : chaque bouton est assigné à un enfant dont on donne le même nom de classe+'-options' (pour faire un lien entre le bouton et l'objet affiché).
//On demande alors simplement d'afficher ce bloc tout en prenant soin de supprimer toutes les popup qui ont pu être ouvertes.
// nom : click_on_popup_button. Par ailleurs on peut donner un attribut qui caractérise tous ces bouttons qui mènent à une popup JS.










//options.onclick = parameters;

function parameters(event){ 
    /*si on clique sur autre chose que display_options, engrenage ou + 
     on cache ou tous les éléments affichés
      return
    si on clique sur engrenage
    display_options.hidden = !display_options.hidden; 
    si on clique sur +, autre elt apparait
    si on clique sur display_options
    si je clique sur un lien cliquable quand la fenêtre est ouverte ça enlève juste la fenêtre, le lien est inactif.
    */

    //
    
    //si on est sur la page initiale 
    if (parameters_options.hidden === true){
        //et qu'on ne clique pas sur un des boutons menant à une popup
        if (!options.contains(event.target) && event.target != id_newcount) return;

        if (options.contains(event.target)) toggle(parameters_options);  display_block_for_children(parameters_options);
        if (event.target === create_tricount) toggle(create_tricount); display_block_for_children(create_tricount);

    } else {
        //si on ne clique pas sur le pop up qui vient de s'ouvrir.
        if (!parameters_options.contains(event.target)){
            desactive_links_when_PopUp_opened(event);
        } else { 
            //PB il faut aussi que si help options est affiché quand on clique ailleurs la pop up disparaisse.
            toggle(parameters_options);
            if (event.target === help){
                toggle(help_options);
                display_block_for_children(help_options);
            }
        }
    }
}

function IsaPopUpDisplayed(){

}

function clickBehaviourForNativePage(){
    /* Fonction qui donne le comportement de clic lorsqu'aucune pop-up n'est ouverte */
}

function clickBehaviourWhenPopUpOpened(event,popup){
    /* Fonction qui donne le comportement de clic lorsqu'aucune pop-up n'est ouverte
    Inputs : event, l'événement.
            popup : l'élément html correspondant à la popup qui s'est ouverte?
    */
    
    //si on ne clique pas sur le pop up qui vient de s'ouvrir, la popup disparait
    if (!popup.contains(event.target)){
        desactive_links_and_close_popup(event,popup);
    } else { 
        //si on clique sur un des boutons de la popup, on remplace la popup affiché par la nouvelle popup.
        replace_popup_by_popup_clicked(event, popup);
    }
}



function toggle(elem){
    elem.hidden = !elem.hidden;
}

function display_block_for_children(elem){
    for (let child of elem.children){
        child.style.display = "block";
    }
}

function replace_popup_by_popup_clicked(event,popup){
    /*Fonction qui remplace par la popup par la popup correspondant au bouton sur lequel on a cliqué */
    let popup_buttons = popup.querySelectorAll('button');
    toggle(popup);
    if (event.target === help){
        toggle(help_options);
        display_block_for_children(help_options);
    }
}

function desactive_links_and_close_popup(event, popup){
    /*Function called when one of the hidden elements are displayed : it prevents from 
    executing links if we click on them*/

    event.preventDefault();
    popup.hidden = true;
    //parameters_options.hidden = true;
    //create_tricount.hidden = true;
}