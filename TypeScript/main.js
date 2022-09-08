// ----- Selector -----
var form = document.querySelector("#new-employee-form"); // selects the first input element
var input = document.querySelector("#new-employee-input");
var list_element = document.querySelector("#employees");
var header = document.querySelector("header");
var submit_button = document.querySelector("#new-employee-submit");
var todoList = document.querySelector(".employee");
// ----- Event Listeners -----
// submit_button.addEventListener('click', addName);
if (!form) {
    console.log("cannot found form");
}
else {
    form.addEventListener("submit", addNew);
}
if (!list_element) {
    console.log("cannot found list element");
}
else {
    list_element.addEventListener("click", check);
}
// ----- Functions -----
// create element and add to class
function createElWithClass(newEl, newClass) {
    var current = document.createElement(newEl);
    current.classList.add(newClass);
    return current;
}
function addNew(e) {
    e.preventDefault(); // stop from refresh the page
    var employee = input.value;
    if (!header) {
        console.log("cannot found header");
        return;
    }
    if (!employee) {
        var incorrectSub_1 = document.createElement("p");
        incorrectSub_1.textContent = "Please insert the employee name";
        incorrectSub_1.style.color = "#E74C3C";
        header.appendChild(incorrectSub_1);
        // disappear after 2s
        setTimeout(function () {
            header.removeChild(incorrectSub_1);
        }, 2000);
        return;
    }
    var employee_element = createElWithClass("div", "employee");
    var employee_content = createElWithClass("div", "content");
    var employee_input = createElWithClass("input", "text");
    employee_input.type = "text";
    employee_input.value = employee;
    employee_input.setAttribute("readonly", "readonly");
    var employee_action = createElWithClass("div", "actions");
    var employee_edit = createElWithClass("button", "edit");
    employee_edit.innerHTML = "Edit";
    var employee_delete = createElWithClass("button", "delete");
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
    input.value = ""; // clean the value after append
    employee_edit.addEventListener("click", function () {
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
    employee_delete.addEventListener("click", function () {
        if (confirm("Are you sure to kick this person out?")) {
            list_element.removeChild(employee_element);
        }
    });
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
function check(e) {
    console.log(e.target);
}
window.addEventListener("load", function () {
    if (!form) {
        console.log("cannot found form");
        return;
    }
    form.addEventListener("submit", function (e) {
        e.preventDefault(); // stop from refresh the page
        // console.log("submit success");
        if (!input) {
            console.log("cannot found input");
            // alert("please enter something ");
            return;
        }
        var employee = input.value;
        // console.log("you entered: " + employee);
        if (!header) {
            console.log("cannot found header");
            return;
        }
        if (!employee) {
            var incorrectSub_2 = document.createElement("p");
            incorrectSub_2.textContent = "Please insert the employee name";
            incorrectSub_2.style.color = "#E74C3C";
            header.appendChild(incorrectSub_2);
            // disappear after 2s
            setTimeout(function () {
                header.removeChild(incorrectSub_2);
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
        var employee_element = createElWithClass("div", "employee");
        var employee_content = createElWithClass("div", "content");
        var employee_input = createElWithClass("input", "text");
        employee_input.type = "text";
        employee_input.value = employee;
        employee_input.setAttribute("readonly", "readonly");
        var employee_action = createElWithClass("div", "actions");
        var employee_edit = createElWithClass("button", "edit");
        employee_edit.innerHTML = "Edit";
        var employee_delete = createElWithClass("button", "delete");
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
        input.value = ""; // clean the value after append
        employee_edit.addEventListener("click", function () {
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
        employee_delete.addEventListener("click", function () {
            if (confirm("Are you sure to kick this person out?")) {
                list_element.removeChild(employee_element);
            }
        });
    });
});
