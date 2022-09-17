import { Employee, EmployeeCreate } from "./model";

// all functions that interact with db

export async function addDB (newEmployee: EmployeeCreate) {
    console.log("inPOST");
    console.log("newEmployee: " + newEmployee);
    console.log( JSON.stringify(newEmployee));
    await fetch('http://127.0.0.1:8000/employee', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newEmployee)
    })
}


export async function readDB (setEmployees: React.Dispatch<React.SetStateAction<Employee[]>>) {
    const response = await fetch("http://127.0.0.1:8000/employee");
    console.log(response);
    const employees = await response.json() as Employee[];
    console.log("employees");
    console.log(employees);
    setEmployees(employees);
}

export async function getIdByName(name: string){
    const response = await fetch("http://127.0.0.1:8000/employee");
    console.log(response);
    const employees = await response.json() as Employee[];
    const db_emp = employees.find(employee => employee.name === name);
    if(db_emp){
        return db_emp.id;
    } else {
        throw new Error("Employee does not exist in db.");
    }
}

export async function updateById (id:number, modiEmp:EmployeeCreate){
    console.log("in updateById");
    await fetch(`http://127.0.0.1:8000/employee/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(modiEmp)
    })
}

export async function deleteById (id:number){
    console.log("deleteById");
    await fetch(`http://127.0.0.1:8000/employee/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        // body:  id
    })
}