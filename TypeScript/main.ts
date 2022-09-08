// ----- Selector -----
const form : HTMLElement | null = document.querySelector("#new-employee-form");        // selects the first input element
const input = document.querySelector("#new-employee-input") as HTMLInputElement;
const list_element = document.querySelector("#employees");
const header = document.querySelector("header");
const submit_button = document.querySelector("#new-employee-submit") as HTMLButtonElement;
const todoList = document.querySelector(".employee");


// ----- Event Listeners -----
// submit_button.addEventListener('click', addName);
if (!form) {
    console.log("cannot found form");
} else {
    form.addEventListener("submit", addNew);
}

if (!list_element) {
    console.log("cannot found list element");
} else {
    list_element.addEventListener("click", check);
}




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
    }

    list_element.appendChild(employee_element);
    
    input.value = "";       // clean the value after append

    employee_edit.addEventListener("click", ()=>{
        if (employee_input.readOnly) {
            employee_input.removeAttribute("readonly");
            employee_input.focus();
            employee_edit.innerText = "Save";
        } else {
            console.log ("Save");
            employee_input.setAttribute("readonly", "readonly");
            employee_edit.innerText = "Edit";
        }

    })

    employee_delete.addEventListener("click", () => {
        if(confirm("Are you sure to kick this person out?")){
            list_element.removeChild(employee_element);
        }
    })
}

// function addName(event:Event) {
//     event.preventDefault();
//     // console.log("click");

//     const todo_div = createElWithClass("div", "employee");

//     const new_todo = createElWithClass("li", "content");
//     new_todo.innerText = 'hey';

//     todo_div.appendChild(new_todo);

//     const employee_edit = createElWithClass("button", "edit");
//     employee_edit.innerHTML = "Edit";

//     const employee_delete = createElWithClass("button", "delete");
//     employee_delete.innerHTML = "Delete";

//     todo_div.appendChild(employee_edit);
//     todo_div.appendChild(employee_delete);

//     if (!list_element) {
//         console.log("cannot found list element");
//         return;
//     }
        
//     list_element.appendChild(todo_div);

// }

function check(e:Event){
    console.log(e.target);
    const item = <HTMLElement> e.target;
    if (item.classList[0] === "delete") {
        const employee_element = <HTMLElement>item.parentElement;
        list_element.removeChild(employee_element);
    }
}

window.addEventListener("load", () => {
    
    if (!form) {
        console.log("cannot found form");
        return;
    }

    form.addEventListener("submit", (e) => {
        e.preventDefault();         // stop from refresh the page

        // console.log("submit success");
        if (!input) {
            console.log("cannot found input");
            // alert("please enter something ");
            return;
        }

        const employee : string | null = input.value;

        // console.log("you entered: " + employee);

        
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

        // if (employee){
        //     console.log("you entered: " + employee);
        // } else {
        //     console.log("Nothing entered!");
        //     alert("please enter something ");
        //     return;
        // }

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
        }

        list_element.appendChild(employee_element);
        
        input.value = "";       // clean the value after append

        employee_edit.addEventListener("click", ()=>{
            if (employee_input.readOnly) {
                employee_input.removeAttribute("readonly");
                employee_input.focus();
                employee_edit.innerText = "Save";
            } else {
                console.log ("Save");
                employee_input.setAttribute("readonly", "readonly");
                employee_edit.innerText = "Edit";
            }

        })

        employee_delete.addEventListener("click", () => {
            if(confirm("Are you sure to kick this person out?")){
                list_element.removeChild(employee_element);
            }
        })
    })
    
})