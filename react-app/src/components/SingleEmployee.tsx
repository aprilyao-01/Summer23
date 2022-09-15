import React, { useEffect, useRef, useState } from 'react'
import { Employee } from './model'

type Props = {
  employee: Employee;
  employees: Employee[];
  setEmployees: React.Dispatch<React.SetStateAction<Employee[]>>;
}


const SingleEmployee = ({employee,employees,setEmployees} : Props) => {
  const [isDelete, setDelete] = useState<boolean>(false);
  const [isEdit, setEdit] = useState<boolean>(false);
  const [editName, setEditName] = useState<string>(employee.name);

  const employeeRef = useRef<HTMLDivElement>(null);      // <div .employee>
  const editBtn = useRef<HTMLButtonElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.focus();    // when isEdit changes(i.e. after click button, give input focus)
  }, [isEdit]);

  useEffect(() => {
    employeeRef.current?.addEventListener('transitionend', function(){
      console.log("classNAme: " + employeeRef.current?.className);
      if (employeeRef.current?.className == 'employee-fall'){
        afterFall(employee.id);     // remove after transition end)
        console.log("id: " + employee.id);
        console.log("after Fall");
      }
      

      // removeLocalName(employee_input.value);
      // employee_element.remove();      // remove after transition end)
    })
  }, [isDelete]);

  const handleDelete =(dele:number) => {
    console.log('in delete');
    if(window.confirm('Are you sure to kick this person out?')){
      // console.log('setTrue');
      setDelete(true);
      // setEmployees(employees.filter(employee => employee.id!== dele));   // only keep the rest
      // console.log(employees);

    }
  }

  const handleTransitionEnd = () => {
    console.log('end');
    // setEmployees(employees.filter(employee => employee.id!== id));    // only keep the rest
  }

  const handleEdit = (edit:number) => {
    if(isEdit === false){
      setEdit(true);
      if (editBtn.current){ editBtn.current.innerText = 'Save'; }
      console.log(employees);
    } else {
      console.log ('Save');
      setEmployees(
        employees.map((employee) => 
        (employee.id === edit ? {...employee, name: editName} : employee))
      );
      setEdit(false);
      if (editBtn.current){ editBtn.current.innerText = 'Edit'; }
      console.log(employees);
    }
  }

  function afterFall(id: number) {
    setEmployees(employees.filter(employee => employee.id !== id));   // only keep the rest
  }

  return (
    <div className={isDelete ? 'employee-fall' : 'employee'} 
      ref={employeeRef}
      >

      <div className='content'>
        <input className='text' 
              type='text' 
              value={editName} 
              readOnly={isEdit ? false : true}
              onChange={(e) => setEditName(e.target.value)}
              ref={inputRef}
        />
      </div>

      <div className='actions'>
       <button className='edit' 
              onClick={() => handleEdit(employee.id)} 
              ref={editBtn}>Edit
        </button>
       <button className='delete' onClick={() => handleDelete(employee.id)}>Delete</button>
      </div>

    </div>
  )
}

export default SingleEmployee


