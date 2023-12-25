let header = document.querySelector('header');
let select = header.querySelector('p');
let backtonewcount = document.querySelector('.backtonewcount');
let loupe = document.querySelector('.currencyresearch');
let research = document.querySelector('.research');
let currencies = document.querySelectorAll('a[name = "link-newcount"]');

header.addEventListener("click", userClicking);
research.addEventListener("input",userSearching);

function userClicking(event){
    if (!backtonewcount.contains(event.target) && event.target.tagName != 'BUTTON') return;

    //Clic sur la loupe fait apparaître la barre de recherche.
    if (event.target.id === "loupe"){
        toggleHeader();
    } 
 
    //Clic sur le retour quand la barre de recherche est là.  
    if (loupe.hidden === true && backtonewcount.contains(event.target)){
        event.preventDefault();
        toggleHeader();
    } 
}

function userSearching(event){
    for (let currency of currencies){  
        hideOrPrintCurrency(currency,event.target.value); 
    }
}

function toggleHeader(){
    /*Function which toggle the header when we wants to do a research or no*/
    research.hidden = !research.hidden;
    select.hidden = !select.hidden;
    loupe.hidden = !loupe.hidden;
}

function hideOrPrintCurrency(currency, string){
    /*Function which hides or prints the currency if it contains the string or not.  
    
    Inputs : 
        - currency (html element <a>) : contains the currency acronym et entire writting
        - string (str)    
    */

    let acronym = currency.querySelector(".acronym").textContent;
    let entire = currency.querySelector(".currencyentire").textContent; 

    if (acronym.includes(string) || entire.includes(string) || acronym.includes(majuscule(string)) || entire.includes(majuscule(string))){ 
        currency.style.display = 'flex';
    } else {
        currency.style.display = 'none';
    } 
}

function majuscule(chaine){
    /*Function which puts the first letter in majuscule*/
    return chaine[0].toUpperCase() + chaine.slice(1)
} 


