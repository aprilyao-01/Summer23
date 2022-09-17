export interface Employee {
    id: number;
    name: string;
    salary?: number;
    dept_id?: number;
    mng_id?: number;
}

export interface EmployeeCreate {
    name: string;           // only has input form for name now :(
}