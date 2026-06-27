from fastapi import APIRouter, HTTPException
from app.database import supabase

router = APIRouter()

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