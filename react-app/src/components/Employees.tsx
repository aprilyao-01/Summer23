import React from 'react'
import { Employee } from './model';
import SingleEmployee from './SingleEmployee';

interface Props{
  employees: Employee[];
  setEmployees:  React.Dispatch<React.SetStateAction<Employee[]>>;
}

const Employees: React.FC<Props> = ({employees, setEmployees} : Props) => {
  return (
    <div id='employees'>
      {employees.map(employee => (
        <SingleEmployee employee={employee} 
          key={employee.id}
          employees={employees}
          setEmployees={setEmployees}/>
      ))}
    </div>
  )
}

export default Employees