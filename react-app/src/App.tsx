import React, { useState } from 'react';
import InputForm from './components/InputForm';
import './App.css';
import HeadTitle from './components/HeadTitle';
import { Employee } from './components/model';
import Employees from './components/Employees';
import EmptyAlert from './components/EmptyAlert';

const App: React.FC = () => {

  const [employee, setEmployee] = useState<string>('');   // #new-employee-input -> input
  const [employees, setEmployees] = useState<Employee[]>([]);   // #employees -> list-element
  const [emptyInput, setEmptyInput] = useState<boolean>(false);

  console.log(employee);

  // get the input value and add a new employee
  const handleAddNew = (e:React.FormEvent) => {
    e.preventDefault();         // stop from refresh the page
  
    if(employee) {
      setEmptyInput(false);
      setEmployees([...employees, {id: Date.now(), name: employee}]);
      setEmployee('');
    } else {
      setEmptyInput(true);
      console.log('Please insert the employee name'); // TODO
      console.log('isEmpty inAPP ' + emptyInput);
    }

    console.log(employees);
  }

  return (
    <div>
      <header>
        <HeadTitle />
        <InputForm employee={employee} setEmployee = {setEmployee} handleAddNew = {handleAddNew}/>
        <EmptyAlert isEmpty= {emptyInput} />
      </header>

      <section className='employee-list'>
        <h2> Employee name</h2>
        <Employees employees={employees} setEmployees={setEmployees}/>
      </section>
    </div>
    
  );
}

export default App;