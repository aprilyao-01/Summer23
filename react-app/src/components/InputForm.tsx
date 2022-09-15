import React, { useRef } from 'react'
import DropDown from './DropDown'

interface Props {
  employee: string;
  setEmployee: React.Dispatch<React.SetStateAction<string>>;
  handleAddNew: (e:React.FormEvent) => void;   // function return nothing
}

const InputForm = ({employee, setEmployee, handleAddNew} : Props) => {
  const inputRef = useRef<HTMLInputElement>(null);      // #new-employee-input input

  return (
    <form id = 'new-employee-form' onSubmit={(e) => {
      handleAddNew(e)
      inputRef.current?.blur();     // remove the focus effect if push enter
    }}> 
      <DropDown />
      <input id='new-employee-input'
            type='input'
            ref={inputRef}
            value={employee}
            onChange={ (e)=>setEmployee(e.target.value) }
            placeholder='Hire someone to work for you (for free) :)' />
      <button type='submit' id='new-employee-submit'> Add employee </button>
    </form>
  )
}

export default InputForm