// ----- Selector -----
const form : HTMLElement | null = document.querySelector("#new-employee-form");        // selects the first input element
const input = document.querySelector("#new-employee-input") as HTMLInputElement;
const list_element = document.querySelector("#employees");
const header = document.querySelector("header");
const dropdowns = document.querySelectorAll<HTMLElement>(".dropdown");

// ----- Event Listeners -----
if (form) { 
    form.addEventListener("submit", addNew); 
}


if (list_element) {
    list_element.addEventListener("click", editNDelete);
}

dropdowns.forEach(dropdown => {
    const select = dropdown.querySelector(".select")as HTMLElement;
    const icon = dropdown.querySelector(".icon")as HTMLElement;
    const menu = dropdown.querySelector(".menu") as HTMLElement;
    const options = dropdown.querySelectorAll<HTMLElement>(".menu li");
    const selected = dropdown.querySelector(".selected") as HTMLElement;

    select.addEventListener("click", () => {
        select.classList.toggle("select-clicked");  //add clicked select style to the select element
        icon.classList.toggle("icon-rotate");      // add rotate style to icon
        menu.classList.toggle("menu-open");        // add open style to menu
    });

    options.forEach(option => {
        option.addEventListener("click",()=>{
            selected.innerText = option.innerText;      // change the inner text to clicked option's inner text
            select.classList.remove("select-clicked");  // remove the clicked select style
            select.classList.remove("icon-rotate");     // remove rotate style to icon
            menu.classList.remove("menu-open");         // remove open style to the menu
            
            options.forEach(option => {
                option.classList.remove("active");      // remove active class from all options
            });

            option.classList.add("active");             // add active style to this clicked option
        });
    });
})


// ----- Functions -----

// create element and add to class
function createElWithClass(newEl:string, newClass:string) {
    const current = document.createElement(newEl)
    current.classList.add(newClass)
    return current
}


function addNew(e: Event) {
    e.preventDefault();         // stop from refresh the page

    const employee : string | null = input.value;

    if (!header) {
        console.log("cannot found header");
        return;
    }

    if (!employee) {
        const incorrectSub = document.createElement("p")
        incorrectSub.textContent = "Please insert the employee name"
        incorrectSub.style.color = "#E74C3C";
        header.appendChild(incorrectSub);

        // disappear after 2s
        setTimeout(function(){
            header.removeChild(incorrectSub);
        }, 2000);
        return;
    }

    const employee_element = createElWithClass("div", "employee");

    const employee_content = createElWithClass("div", "content");

    const employee_input = <HTMLInputElement> createElWithClass("input", "text");
    employee_input.type = "text";
    employee_input.value = employee;
    employee_input.setAttribute("readonly", "readonly");

    const employee_action = createElWithClass("div", "actions");

    const employee_edit = createElWithClass("button", "edit");
    employee_edit.innerHTML = "Edit";

    const employee_delete = createElWithClass("button", "delete");
    employee_delete.innerHTML = "Delete";

    employee_content.appendChild(employee_input);

    employee_action.appendChild(employee_edit);
    employee_action.appendChild(employee_delete);
    
    employee_element.appendChild(employee_content);
    employee_element.appendChild(employee_action);
    
    if (!list_element) {
        console.log("cannot found list element");
        return;
    } else {
        list_element.appendChild(employee_element);
    }

    input.value = "";       // clean the value after append
}


// edit employee name or delete the employee
function editNDelete(e:Event){
    console.log(e.target);
    const item = <HTMLElement> e.target;
    const employee_action = <HTMLElement>item.parentElement;
    const employee_element = <HTMLElement>employee_action.parentElement;

    if (item.classList[0] === "delete") {  
        if(confirm("Are you sure to kick this person out?")){
            employee_element.classList.toggle("employee-fall");      // add animation
            
            employee_element.addEventListener("transitionend", function(){
                employee_element.remove();      // remove after transition end
            })
            
        }
    }

    if (item.classList[0] === "edit") {  
        const employee_input = <HTMLInputElement>employee_element.querySelector(".text");
        if (employee_input.readOnly) {
            employee_input.removeAttribute("readonly");
            employee_input.focus();
            item.innerText = "Save";
        } else {
            console.log ("Save");
            employee_input.setAttribute("readonly", "readonly");
            item.innerText = "Edit";
        }
    }
}

// window.addEventListener("load", () => {
    
//     if (!form) {
//         console.log("cannot found form");
//         return;
//     }

//     form.addEventListener("submit", (e) => {
//         e.preventDefault();         // stop from refresh the page

//         // console.log("submit success");
//         if (!input) {
//             console.log("cannot found input");
//             // alert("please enter something ");
//             return;
//         }

//         const employee : string | null = input.value;

//         // console.log("you entered: " + employee);

        
//         if (!header) {
//             console.log("cannot found header");
//             return;
//         }

//         // if (!employee) {
//         //     const incorrectSub = document.createElement("p")
//         //     incorrectSub.textContent = "Please insert the employee name"
//         //     incorrectSub.style.color = "#E74C3C";
//         //     header.appendChild(incorrectSub);

//         //     // disappear after 2s
//         //     setTimeout(function(){
//         //        header.removeChild(incorrectSub);
//         //     }, 2000);
            
//         //     return;
//         // }

//         // if (employee){
//         //     console.log("you entered: " + employee);
//         // } else {
//         //     console.log("Nothing entered!");
//         //     alert("please enter something ");
//         //     return;
//         // }

//         const employee_element = createElWithClass("div", "employee");

//         const employee_content = createElWithClass("div", "content");

//         const employee_input = <HTMLInputElement> createElWithClass("input", "text");
//         employee_input.type = "text";
//         employee_input.value = employee;
//         employee_input.setAttribute("readonly", "readonly");

//         const employee_action = createElWithClass("div", "actions");

//         const employee_edit = createElWithClass("button", "edit");
//         employee_edit.innerHTML = "Edit";

//         const employee_delete = createElWithClass("button", "delete");
//         employee_delete.innerHTML = "Delete";

//         employee_content.appendChild(employee_input);

//         employee_action.appendChild(employee_edit);
//         employee_action.appendChild(employee_delete);
        
//         employee_element.appendChild(employee_content);
//         employee_element.appendChild(employee_action);
        
        

//         if (!list_element) {
//             console.log("cannot found list element");
//             return;
//         }

//         list_element.appendChild(employee_element);
        
//         input.value = "";       // clean the value after append

//         employee_edit.addEventListener("click", ()=>{
//             if (employee_input.readOnly) {
//                 employee_input.removeAttribute("readonly");
//                 employee_input.focus();
//                 employee_edit.innerText = "Save";
//             } else {
//                 console.log ("Save");
//                 employee_input.setAttribute("readonly", "readonly");
//                 employee_edit.innerText = "Edit";
//             }

//         })

//         employee_delete.addEventListener("click", () => {
//             if(confirm("Are you sure to kick this person out?")){
//                 list_element.removeChild(employee_element);
//             }
//         })
//     })
    
// })