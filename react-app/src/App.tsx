import React, { createContext, useContext, useEffect, useState } from 'react';
import InputForm from './components/InputForm';
import './App.css';
import HeadTitle from './components/HeadTitle';
import { Employee } from './components/model';
import Employees from './components/Employees';
import { readDB, getIdByName, addDB } from './components/operation';


const App: React.FC = () => {

  const [input, setInput] = useState<string>('');   // #new-employee-input -> input
  const [employees, setEmployees] = useState<Employee[]>([]);   // #employees -> list-element
  const [isShow, setIsShow] = useState<boolean>(false);

  useEffect(() => {
    readDB(setEmployees);    // Read all from db and initialize when page loaded
    console.log('app initialized');
  },[])

  // get the input value and add a new employee
  const handleAddNew = async (e:React.FormEvent) => {
    e.preventDefault();         // stop from refresh the page
  
    if(input) {
      setIsShow(false);
      await addDB({name: input});      // POST in backend
      const id = await getIdByName(input);      // GET id from backend
      setEmployees([...employees, {id: id, name: input}]);
      setInput('');
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
        <InputForm employee={input} setEmployee = {setInput} handleAddNew = {handleAddNew}/>
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