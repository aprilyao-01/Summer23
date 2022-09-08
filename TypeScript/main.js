window.addEventListener('load', function () {
    var form = document.querySelector("#new-employee-form");
    var input = document.querySelector("#new-employee-input");
    var list_element = document.querySelector("#employees");
    if (!form) {
        console.log("cannot found form");
        return;
    }
    form.addEventListener('submit', function (e) {
        e.preventDefault(); // stop from refresh the page
        // console.log("submit success");
        if (!input) {
            console.log("cannot found input");
            // alert("please enter something ");
            return;
        }
        var employee = input.value;
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
        var employee_element = document.createElement("div");
        employee_element.classList.add("employee");
        var employee_content = document.createElement("div");
        employee_content.classList.add("content");
        var employee_input = document.createElement("input");
        employee_input.classList.add("text");
        employee_input.type = "text";
        employee_input.value = employee;
        employee_input.setAttribute("readonly", "readonly");
        var employee_action = document.createElement("div");
        employee_action.classList.add("actions");
        var employee_edit = document.createElement("button");
        employee_edit.classList.add("edit");
        employee_edit.innerHTML = "Edit";
        var employee_delete = document.createElement("button");
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
        input.value = ""; // clean the value
        employee_edit.addEventListener('click', function () {
            if (employee_input.readOnly) {
                employee_input.removeAttribute("readonly");
                employee_input.focus();
                employee_edit.innerText = "Save";
            }
            else {
                console.log("Save");
                employee_input.setAttribute("readonly", "readonly");
                employee_edit.innerText = "Edit";
            }
        });
        employee_delete.addEventListener('click', function () {
            if (confirm("Are you sure to kick this person out?")) {
                list_element.removeChild(employee_element);
            }
        });
    });
});
