window.addEventListener('DOMContentLoaded', () => {
    // Get all possible popups initially hidden
    let elemtsInitiallyHidden = document.body.querySelectorAll('[data-div = hidden]'); 

    // Behaviour when clicking on the page
    document.addEventListener("click", (event) => click_on_page(event, elemtsInitiallyHidden));

    // Specific behaviour clicks
    document.querySelector('.parameters').addEventListener("click", (event) => click_on_parameter(event, elemtsInitiallyHidden));
    document.querySelector('.parameters-options').addEventListener("click", click_on_parameter_options);
    document.querySelector('.id_newcount').addEventListener("click", (event) => click_on_newcount(event, elemtsInitiallyHidden));
    document.querySelector('.choosecount').addEventListener("click", click_on_choose_count);

    // Event when submitting clonecount form
    document.querySelector('.form-pwdcount form').addEventListener("submit", click_on_submit); 
})

/*Events handlers */
function click_on_parameter(event, elemtsInitiallyHidden) { 
    // Do nothing if a popup is opened
    if (isOnePopUpApparent(elemtsInitiallyHidden)) return;

    // Display a popup if click on parameter
    if (event.currentTarget == document.querySelector('.parameters')){ 
        toggle(document.querySelector('.parameters-options'));  
        style_display_block_for_children(document.querySelector('.parameters-options'));
        
        // Prevent goback from being launched
        event.stopPropagation();
    }
}

function click_on_parameter_options(event){
    // Do nothing if click on other then a button
    if (!event.target.dataset.button) return; 

    // Display the child element the user clicks on 
    toggle(document.querySelector('.parameters-options'));  
    toggle(document.querySelector(`.${event.target.className}-options`));
    style_display_block_for_children(document.querySelector(`.${event.target.className}-options`));

    // Prevent goback from being launched
    event.stopPropagation();
}

function click_on_page(event, elemtsInitiallyHidden){ 
    // Do nothing if a popup is opened
    if (!isOnePopUpApparent(elemtsInitiallyHidden)) return;

    // Hide all opened popups if the user does not click on it
    if (!event.target.closest('div')?.dataset.div){ 
        event.preventDefault(); 
        hide_all_popup_elements(elemtsInitiallyHidden);
    }
}


/*Utilities */
function toggle(elem){
    elem.hidden = !elem.hidden;
}

function isOnePopUpApparent(elemtsInitiallyHidden){
    /* Returns true of a popup is opened */
    let bool = false;
    for (elem of elemtsInitiallyHidden){ 
        if (elem.hidden === false){ 
            bool = true;
        }
    }  
    return bool;
}

function hide_all_popup_elements(elemtsInitiallyHidden){
    for (elem of elemtsInitiallyHidden) elem.hidden = true;
}

function style_display_block_for_children(elem){
    for (let child of elem.children){
        child.style.display = "block";
    }
}

function click_on_newcount(event, elemtsInitiallyHidden){
    // Do nothing if a popup or the last form are opened
    if (isOnePopUpApparent(elemtsInitiallyHidden)) return;
    if (!document.querySelector('.form-pwdcount').hidden) return;

    // Display a popup to choose the way to create a tricount
    document.querySelector('.choosecount').hidden = false;
    event.stopPropagation();
}

function click_on_choose_count(event){
    /* Open the form to clone an existing tricount*/  
    if (event.target != document.body.querySelector('.clonecount')) return;
    document.querySelector('.choosecount').hidden = true;
    document.querySelector('.form-pwdcount').hidden = false;  
    event.stopPropagation();
}

function click_on_submit(event){
    /* Display an error message if the user does not fill an input in the clone count form */
    if (document.querySelector('.password').value !== "Mot de passe du tricount" 
        && document.querySelector('.password').value !== "" 
        && document.querySelector('.tricount-title').value !== "Titre du tricount" 
        && document.querySelector('.tricount-title').value !== "") return;    
    
    // Create an error message
    event.preventDefault(); 
    document.querySelector('.error').hidden = false; 
    
    // Clear inputs
    document.querySelector('.tricount-title').value = ''; 
    document.querySelector('.password').value = ''; 
}