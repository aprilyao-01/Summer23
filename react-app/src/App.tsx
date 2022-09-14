import React, { useState } from 'react';
import InputFelid from './components/InputFelid';
import "./App.css";
import HeadTitle from './components/HeadTitle';
import { Employee } from './components/model';



function handleAddNew(e:React.FormEvent) {
  e.preventDefault();         // stop from refresh the page

  // const employee : string | null = input.value;


  // if (!employee) {
  //     const incorrectSub = document.createElement('p')
  //     incorrectSub.textContent = 'Please insert the employee name'
  //     incorrectSub.style.color = '#E74C3C';
  //     header.appendChild(incorrectSub);

  //     // disappear after 2s
  //     setTimeout(function(){
  //         header.removeChild(incorrectSub);
  //     }, 2000);
  //     return;
  // }

  // const employee_element = createElWithClass('div', 'employee');

  // const employee_content = createElWithClass('div', 'content');

  // const employee_input = <HTMLInputElement> createElWithClass('input', 'text');
  // employee_input.type = 'text';
  // employee_input.value = employee;
  // employee_input.setAttribute('readonly', 'readonly');

  // const employee_action = createElWithClass('div', 'actions');

  // const employee_edit = createElWithClass('button', 'edit');
  // employee_edit.innerHTML = 'Edit';

  // const employee_delete = createElWithClass('button', 'delete');
  // employee_delete.innerHTML = 'Delete';

  // employee_content.appendChild(employee_input);

  // employee_action.appendChild(employee_edit);
  // employee_action.appendChild(employee_delete);
  
  // employee_element.appendChild(employee_content);
  // employee_element.appendChild(employee_action);
  
  // if (!list_element) {
  //     console.log('cannot found list element');
  //     return;
  // } else {
  //     list_element.appendChild(employee_element);
  // }

  // saveLocalName(employee);

  // input.value = '';       // clean the value after append
}


const App: React.FC = () => {

  const [employee, setEmployee] = useState<string>("");
  const [employees_list, setEmployeesList] = useState<Employee[]>([]);

  return (
    <div>
      <header>
        <HeadTitle />
        <InputFelid employee={employee} setEmployee = {setEmployee} handleAddNew = {handleAddNew}/>
      </header>
    </div>
    
  );
}

export default App;
