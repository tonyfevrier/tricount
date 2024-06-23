const form = document.querySelector('form');
const input = document.querySelector("input[type = 'text']");
const main = document.querySelector("main");

let current_date = "";

window.addEventListener("DOMContentLoaded", () => {
    const user = prompt("enter your username");
    const websocket = new WebSocket(`ws://localhost:8001/?user=${user}`);
    sendMsg(websocket);
    receiveMsg(websocket);
});


function sendMsg(websocket){ 
    form.addEventListener("submit", (event) => {
        //on envoie le message et l'utilisateur au serveur 
        event.preventDefault(); 
        message = input.value; 
        if (message == "") return;

        let msg = {text : message, user : getParamsWs(websocket)};
        websocket.send(JSON.stringify(msg));
        input.value = "";
    }); 
}

function receiveMsg(websocket){ 
    //on crée un élément div avec le message qu'on ajoute à l'html
    websocket.addEventListener("message", ({data})=>{ 
        const event = JSON.parse(data);  
        const popup = document.createElement('div');
        popup.innerHTML = `<p class = "popupuser">${event.user}</p> <p class = "popuptext">${event.text}</p>  <p class = "popuphour">${event.hour}</p>`;
        
        //si c'est moi qui envoie le message, le css sera différent.
 
        if (event.user == getParamsWs(websocket)){
            popup.className = "owner-popup";
        } else {
            popup.className = "popup";
        }
        date = printDate(event);
        if (date) main.append(date);
        main.append(popup);
    });
}

function printDate(event){
    /* Function which prints a div containing the date if it is the first message of the day */

    //on récupère la date de l'évent, si la date est différente d'une variable créee avec la précédente date
    //on crée l'élement sinon on ne fait rien.

    if (event.date != current_date){
        const date = document.createElement('div');
        date.innerHTML = event.date;
        date.className = "daydate";
        current_date = event.date;
        return date;
    } else {
        return;
    }
}

function getParamsWs(websocket){
    /* Function to recover the name of the user from the websocket*/
    const url = new URL(websocket.url);
    const params = new URLSearchParams(url.search); 
    return params.get('user');
}