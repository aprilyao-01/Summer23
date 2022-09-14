import React from 'react'
import DropDown from './DropDown'

interface Props {
  employee: string;
  setEmployee: React.Dispatch<React.SetStateAction<string>>;
  handleAddNew: (e:React.FormEvent) => void;   // function return nothing
}

const InputFelid = ({employee, setEmployee, handleAddNew} : Props) => {
  return (
    <form id = 'new-employee-form' onSubmit={handleAddNew}> 
      <DropDown />
      <input type='input'
            id="new-employee-input"
            value={employee}
            onChange={ (e)=>setEmployee(e.target.value) }
            placeholder='Hire someone to work for you (for free) :)' />
      <button type='submit' id='new-employee-submit'> Add employee </button>
    </form>
  )
}

export default InputFelid