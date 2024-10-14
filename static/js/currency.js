window.addEventListener('DOMContentLoaded', () => {

    //The href of the links depends on the referer url : we extract this information and add it to the links 
    const params = new URLSearchParams(window.location.search);

    document.querySelector('.backtonewcount').href = params.get('referer');
    const currencies = document.querySelectorAll('a[name = "link-newcount"]')
    for (let currency of currencies){ 
        currency.href = params.get("referer") +"?currency=" + currency.className; 
    }

    // Event when clicking on the header
    document.querySelector('header').addEventListener("click", user_clicking);

    // Event for research bar
    document.querySelector('.research').addEventListener("input", (event) => user_searching(event, currencies));
})

function user_clicking(event){
    // Do nothing if the click is not on these buttons
    if (!document.querySelector('.backtonewcount').contains(event.target) 
        && !document.querySelector('.currencyresearch').contains(event.target)) return;

    // Clic on research displays a search bar
    if (document.querySelector('.currencyresearch').contains(event.target)){
        toggle_header();
    } 
 
    // Clic on back when the search bar is opened only hide the search bar 
    if (document.querySelector('.currencyresearch').hidden === true 
        && document.querySelector('.backtonewcount').contains(event.target)){
        event.preventDefault();
        toggle_header();
    } 
}

function user_searching(event, currencies){
    /* Displays or hide currencies whether they contain what the user writes or not */ 
    for (let currency of currencies){  
        hide_or_print_currency(currency, event.target.value); 
    }
}

function toggle_header(){
    /*Function which toggle the header when we wants to do a research or no*/
    document.querySelector('.research').hidden = !document.querySelector('.research').hidden;
    document.querySelector('header').querySelector('p').hidden = !document.querySelector('header').querySelector('p').hidden;
    document.querySelector('.currencyresearch').hidden = !document.querySelector('.currencyresearch').hidden;
}

function hide_or_print_currency(currency, string){
    /*Function which hides or prints the currency if it contains the string or not.  
    
    Inputs : 
        - currency (html element <a>) : contains the currency acronym et entire writting
        - string (str)    
    */

    const acronym = currency.querySelector(".acronym").textContent;
    const entire = currency.querySelector(".currencyentire").textContent; 

    if (acronym.includes(string) || entire.includes(string) ||
        acronym.includes(majuscule(string)) || entire.includes(majuscule(string))){ 
        currency.style.display = 'flex';
    } else {
        currency.style.display = 'none';
    } 
}

function majuscule(chaine){
    /*Function which puts the first letter in majuscule*/
    return chaine[0].toUpperCase() + chaine.slice(1)
} 