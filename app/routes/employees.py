from fastapi import APIRouter, HTTPException
from app.database import supabase
from pydantic import BaseModel

router = APIRouter()

class EmployeeCreate(BaseModel):
    name: str
    position: str
    department: str
    salary: float
    employment_history: str
    contact: str

@router.get("/")
def get_employees():
    response = supabase.table("employees").select("*").execute()
    return response.data

@router.get("/{employee_id}")
def get_employee(employee_id: int):
    response = supabase.table("employees").select("*").eq("id", employee_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Employee not found")
    return response.data[0]

@router.post("/")
def create_employee(employee: EmployeeCreate):
    response = supabase.table("employees").insert({
        "name": employee.name,
        "position": employee.position,
        "department": employee.department,
        "salary": employee.salary,
        "employment_history": employee.employment_history,
        "contact": employee.contact
    }).execute()

    if response.data:
        new_emp = response.data[0]
        supabase.table("leave_balances").insert({
            "employee_id": new_emp["id"]
        }).execute()

    return {"message": "Employee created", "data": response.data}