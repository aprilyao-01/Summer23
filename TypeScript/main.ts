window.addEventListener('load', () => {
    const form : HTMLElement | null = document.querySelector("#new-employee-form");
    const input : HTMLInputElement | null  = document.querySelector("#new-employee-input");
    const list_element : HTMLDataListElement | null = document.querySelector("#employees");

    if (!form) {
        console.log("cannot found form");
        return;
    }

    form.addEventListener('submit', (e) => {
        e.preventDefault();         // stop from refresh the page

        // console.log("submit success");
        if (!input) {
            console.log("cannot found input");
            // alert("please enter something ");
            return;
        }

        const employee : string | null = input.value;

        if (!employee) {
            console.log("Nothing entered!");
            alert("please enter something ");
            return;
        }

        console.log("you entered: " + employee);

        // if (employee){
        //     console.log("you entered: " + employee);
        // } else {
        //     console.log("Nothing entered!");
        //     alert("please enter something ");
        //     return;
        // }

        const employee_element = document.createElement("div");
        employee_element.classList.add("employee");

        const employee_content = document.createElement("div");
        employee_content.classList.add("content");

        const employee_input  = document.createElement("input");
        employee_input.classList.add("text");
        employee_input.type = "text";
        employee_input.value = employee;
        employee_input.setAttribute("readonly", "readonly");

        const employee_action = document.createElement("div");
        employee_action.classList.add("actions");

        const employee_edit = document.createElement("button");
        employee_edit.classList.add("edit");
        employee_edit.innerHTML = "Edit";

        const employee_delete = document.createElement("button");
        employee_delete.classList.add("delete");
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
        
        input.value = "";       // clean the value

        employee_edit.addEventListener('click', ()=>{
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

        employee_delete.addEventListener('click', () => {
            if(confirm("Are you sure to kick this person out?")){
                list_element.removeChild(employee_element);
            }
        })
    })
    
})