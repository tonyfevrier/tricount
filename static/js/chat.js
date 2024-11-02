
const main = document.querySelector(".container");

let current_date = "";

window.addEventListener("DOMContentLoaded", () => {  
    document.querySelector('.container').scrollTop = document.querySelector(".container").scrollHeight; 
    const websocket = new WebSocket(`ws://${window.location.host}/chat/${document.querySelector('.header-title').id}/?user=${document.querySelector('.owner').textContent}`);
    sendMsg(websocket);
    receiveMsg(websocket);
});


function sendMsg(websocket){  
    document.querySelector('.submit').addEventListener("click", (event) => { 
        // Get message
        message = document.querySelector('textarea').value;  
        if (message == "") return;

        // Send the message and put the textarea as empty
        const msg = {content : message, writer : getParamsWs(websocket), tricountid : document.querySelector('.header-title').id};
        websocket.send(JSON.stringify(msg));
        document.querySelector('textarea').value = "";
    }); 
}

function receiveMsg(websocket){   
    // A message arrives
    websocket.addEventListener("message", ({data})=>{  
        const event = JSON.parse(data); 

        // Create an element to print the message
        const popup = document.createElement('div');
        popup.innerHTML = `<p class = "user">${event.writer}</p>
                           <p class = "text">${event.content}</p>
                           <p class = "time">${event.time}</p>`; 
        
        // Prepare for different CSS if I am the sender or not 
        if (event.writer == getParamsWs(websocket)){
            popup.className = "owner-popup";
        } else {
            popup.className = "popup";
        }

        date = print_date(event);
        if (date) main.append(date);
        main.append(popup);
        
        document.querySelector('.container').scrollTop = document.querySelector(".container").scrollHeight; 
    });
}

function print_date(event){
    /* Function which prints a div containing the date if it is the first message of the day */   
 
    const date_elements = document.querySelectorAll('.daydate'); 

    // Create a div with date if the date become different from the previous registered date and not already printed
    if (date_elements.length){
        if (event.date != current_date && date_elements[date_elements.length - 1].innerHTML !== event.date){
            return create_date_element(event);
        } 
    } else {
        if (event.date != current_date){
            return create_date_element(event);
        } 
    }
}

function create_date_element(event){
    const date = document.createElement('div');
    date.innerHTML = event.date;
    date.className = "daydate";
    current_date = event.date;
    return date;
}

function getParamsWs(websocket){
    /* Function to recover the name of the user from the websocket */
    const url = new URL(websocket.url);
    const params = new URLSearchParams(url.search); 
    return params.get('user');
}