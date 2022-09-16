import React, { useState } from 'react';
import InputForm from './components/InputForm';
import './App.css';
import HeadTitle from './components/HeadTitle';
import { Employee } from './components/model';
import Employees from './components/Employees';

const App: React.FC = () => {

  const [employee, setEmployee] = useState<string>('');   // #new-employee-input -> input
  const [employees, setEmployees] = useState<Employee[]>([]);   // #employees -> list-element
  const [isShow, setIsShow] = useState<boolean>(false);

  // get the input value and add a new employee
  const handleAddNew = (e:React.FormEvent) => {
    e.preventDefault();         // stop from refresh the page
  
    if(employee) {
      setIsShow(false);
      setEmployees([...employees, {id: Date.now(), name: employee}]);
      setEmployee('');
    } else {
      setIsShow(true);

      setTimeout(function(){
        setIsShow(false);     // disappear after 2s
      }, 2000);
    }

    console.log(employees);
  }

  return (
    <div>
      <header>
        <HeadTitle />
        <InputForm employee={employee} setEmployee = {setEmployee} handleAddNew = {handleAddNew}/>
        {isShow ? (<p id='alert'>Please insert the employee name </p>) : (null)}
      </header>

      <section className='employee-list'>
        <h2> Employee name</h2>
        <Employees employees={employees} setEmployees={setEmployees}/>
      </section>
    </div>
    
  );
}

export default App;