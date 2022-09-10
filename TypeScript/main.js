// ----- Selector -----
var form = document.querySelector('#new-employee-form'); // selects the first input element
var input = document.querySelector('#new-employee-input');
var list_element = document.querySelector('#employees');
var header = document.querySelector('header');
var dropdowns = document.querySelectorAll('.dropdown');
// ----- Event Listeners -----
// get back all local storage when dom content loaded
document.addEventListener('DOMContentLoaded', getLocalName);
form.addEventListener('submit', addNew);
list_element.addEventListener('click', editNDelete);
// dropdown menu event listener
dropdowns.forEach(function (dropdown) {
    var select = dropdown.querySelector('.select');
    var icon = dropdown.querySelector('.icon');
    var menu = dropdown.querySelector('.menu');
    var options = dropdown.querySelectorAll('.menu li');
    var selected = dropdown.querySelector('.selected');
    select.addEventListener('click', function () {
        select.classList.toggle('select-clicked'); //add clicked select style to the select element
        icon.classList.toggle('icon-rotate'); // add rotate style to icon
        menu.classList.toggle('menu-open'); // add open style to menu
    });
    options.forEach(function (option) {
        option.addEventListener('click', function () {
            selected.innerText = option.innerText; // change the inner text to clicked option's inner text
            select.classList.remove('select-clicked'); // remove the clicked select style
            icon.classList.remove('icon-rotate'); // remove rotate style to icon
            menu.classList.remove('menu-open'); // remove open style to the menu
            options.forEach(function (option) {
                option.classList.remove('active'); // remove active class from all options
            });
            option.classList.add('active'); // add active style to this clicked option
        });
    });
});
// ----- Functions -----
// create element and add to class
function createElWithClass(newEl, newClass) {
    var current = document.createElement(newEl);
    current.classList.add(newClass);
    return current;
}
// get the input value and add a new employee
function addNew(e) {
    e.preventDefault(); // stop from refresh the page
    var employee = input.value;
    if (!header) {
        console.log('cannot found header');
        return;
    }
    if (!employee) {
        var incorrectSub_1 = document.createElement('p');
        incorrectSub_1.textContent = 'Please insert the employee name';
        incorrectSub_1.style.color = '#E74C3C';
        header.appendChild(incorrectSub_1);
        // disappear after 2s
        setTimeout(function () {
            header.removeChild(incorrectSub_1);
        }, 2000);
        return;
    }
    var employee_element = createElWithClass('div', 'employee');
    var employee_content = createElWithClass('div', 'content');
    var employee_input = createElWithClass('input', 'text');
    employee_input.type = 'text';
    employee_input.value = employee;
    employee_input.setAttribute('readonly', 'readonly');
    var employee_action = createElWithClass('div', 'actions');
    var employee_edit = createElWithClass('button', 'edit');
    employee_edit.innerHTML = 'Edit';
    var employee_delete = createElWithClass('button', 'delete');
    employee_delete.innerHTML = 'Delete';
    employee_content.appendChild(employee_input);
    employee_action.appendChild(employee_edit);
    employee_action.appendChild(employee_delete);
    employee_element.appendChild(employee_content);
    employee_element.appendChild(employee_action);
    if (!list_element) {
        console.log('cannot found list element');
        return;
    }
    else {
        list_element.appendChild(employee_element);
    }
    saveLocalName(employee);
    input.value = ''; // clean the value after append
}
// remove name from local storage
function removeLocalName(name) {
    var names = []; // list of input text
    var local_name = localStorage.getItem('names');
    if (local_name === null) {
        names = []; // if doesn't exist, create empty list
    }
    else {
        names = JSON.parse(local_name);
    }
    names.splice(names.indexOf(name), 1);
    localStorage.setItem("names", JSON.stringify(names));
}
// edit employee name or delete the employee
function editNDelete(e) {
    console.log(e.target);
    var item = e.target;
    var employee_action = item.parentElement;
    var employee_element = employee_action.parentElement;
    var employee_input = employee_element.querySelector('.text');
    if (item.classList[0] === 'delete') {
        console.log("in delete");
        if (confirm('Are you sure to kick this person out?')) {
            console.log("employee_element: " + employee_element.className);
            employee_element.classList.toggle('employee-fall'); // add animation
            console.log("employee_element: " + employee_element.className);
            employee_element.addEventListener('transitionend', function () {
                removeLocalName(employee_input.value);
                employee_element.remove(); // remove after transition end
            });
        }
    }
    if (item.classList[0] === 'edit') {
        if (employee_input.readOnly) {
            employee_input.removeAttribute('readonly');
            employee_input.focus();
            item.innerText = 'Save';
        }
        else {
            console.log('Save');
            employee_input.setAttribute('readonly', 'readonly');
            item.innerText = 'Edit';
        }
    }
}
// save input to local storage
function saveLocalName(newName) {
    var names = []; // array of input text
    var local_name = localStorage.getItem('names');
    if (local_name !== null) {
        names = JSON.parse(local_name); // make sure it's not null
    }
    else {
        names = []; // if doesn't exist, create empty list
    }
    names.push(newName);
    localStorage.setItem('names', JSON.stringify(names)); // set back to local storage
}
// get local storage name and recreate the UI
function getLocalName() {
    var names = []; // list of input text
    var local_name = localStorage.getItem('names');
    if (local_name === null) {
        names = []; // if doesn't exist, create empty list
    }
    else {
        names = JSON.parse(local_name); // make sure it's not null and get it back
    }
    for (var _i = 0, names_1 = names; _i < names_1.length; _i++) { // replaced forEach
        var name_1 = names_1[_i];
        var employee_element = createElWithClass('div', 'employee');
        var employee_content = createElWithClass('div', 'content');
        var employee_input = createElWithClass('input', 'text');
        employee_input.type = 'text';
        employee_input.value = name_1;
        employee_input.setAttribute('readonly', 'readonly');
        var employee_action = createElWithClass('div', 'actions');
        var employee_edit = createElWithClass('button', 'edit');
        employee_edit.innerHTML = 'Edit';
        var employee_delete = createElWithClass('button', 'delete');
        employee_delete.innerHTML = 'Delete';
        employee_content.appendChild(employee_input);
        employee_action.appendChild(employee_edit);
        employee_action.appendChild(employee_delete);
        employee_element.appendChild(employee_content);
        employee_element.appendChild(employee_action);
        if (!list_element) {
            console.log('cannot found list element');
            return;
        }
        else {
            list_element.appendChild(employee_element);
        }
    }
}
