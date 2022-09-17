import React, { useEffect, useRef, useState } from 'react'
import { Employee } from './model'
import { deleteById, updateById } from './operation';

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
    employeeRef.current?.addEventListener('transitionend', async function(){
      if (employeeRef.current?.className === 'employee-fall'){
        await afterFall(employee.id);     // remove after transition end
      }
    })
  }, [isDelete]);

  const handleDelete =() => {
    if(window.confirm('Are you sure to kick this person out?')){
      setDelete(true);
    }
  }

  const handleEdit = async (editID:number) => {
    if(isEdit === false){
      setEdit(true);
      if (editBtn.current){ editBtn.current.innerText = 'Save'; }
    } else {
      setEmployees(
        employees.map((employee) => 
        (employee.id === editID ? {...employee, name: editName} : employee))
      );
      await updateById(editID, {name: editName});
      setEdit(false);
      if (editBtn.current){ editBtn.current.innerText = 'Edit'; }
    }
  }

  async function afterFall(id: number) {
    setEmployees(employees.filter(employee => employee.id !== id));   // delete the employee from employees
    await deleteById(id);       // DELETE from backend db
    // backend shows '404not found' but it is deleted
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
       <button className='delete' onClick={handleDelete}>Delete</button>
      </div>

    </div>
  )
}

export default SingleEmployee