import React from 'react'

const DropDown = () => {
  return (
    <div className="dropdown">
            <div className="select">
                <span className="selected">Employee</span>
                <div className="icon"></div>
            </div>
            <ul className="menu">
                <li className="active">Employee</li>
                <li>Manager</li>ß
                <li>Department</li>
            </ul>
    </div>
  )
}

export default DropDown