import React, { useRef, useState } from 'react'

const DropDown = () => {
  const [highlight, setHighlight] = useState<boolean>(false);
  const [rotate, setRotate] = useState<boolean>(false);
  const [open, setOpen] = useState<boolean>(false);
  const [activeE, setActiveE] = useState<boolean>(true);
  const [activeM, setActiveM] = useState<boolean>(false);
  const [activeD, setActiveD] = useState<boolean>(false);

  const selectedRef = useRef<HTMLSpanElement>(null);
  const optionERef = useRef<HTMLLIElement>(null);
  const optionMRef = useRef<HTMLLIElement>(null);
  const optionDRef = useRef<HTMLLIElement>(null);

  const handleClick = () => {
    setHighlight(!highlight);
    setRotate(!rotate);
    setOpen(!open);
  }

  const handleSelect = (e: React.MouseEvent<HTMLLIElement>) =>{
    const option = e.target as HTMLLIElement;
    if (selectedRef.current) {
      selectedRef.current.innerText = option.innerText;
    }

    switch (option.innerText) {
      case 'Employee':
        setActiveE(true);
        setActiveM(false);
        setActiveD(false);
        break;
      case 'Manager':
        setActiveM(true);
        setActiveE(false);
        setActiveD(false);
        break;
      case 'Department':
        setActiveD(true);
        setActiveM(false);
        setActiveE(false);
        break;
    }

    setHighlight(!highlight);
    setRotate(!rotate);
    setOpen(!open);
  }
  
  return (
    <div className='dropdown'>
      <div className={`select${highlight ? "-clicked" : ""}`} onClick={handleClick}>
          <span className='selected' ref={selectedRef}>Employee</span>
          <div className= {`icon${rotate ? '-rotate' : ''}`}></div>
      </div>
      <ul className={`menu${open ? '-open' : ''}`}>

          <li className={activeE? 'active' : ''} ref={optionERef} onClick={handleSelect}>Employee</li>
          <li className={activeM? 'active' : ''} ref={optionMRef} onClick={handleSelect}>Manager</li>
          <li className={activeD? 'active' : ''} ref={optionDRef} onClick={handleSelect}>Department</li>
      </ul>
    </div>
  )
}

export default DropDown