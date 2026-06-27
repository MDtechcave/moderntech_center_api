from fastapi import APIRouter
from app.database import supabase

router = APIRouter()

@router.get("/")
def get_attendance():
    response = supabase.table("attendance").select("*, employees(name)").execute()
    return response.data

@router.get("/leave")
def get_leave_requests():
    response = supabase.table("leave_requests").select("*").execute()
    return response.data

@router.get("/{employye_id}")
def get_employee_attendance(employee_id: int):
    response = supabase.table("attendance").select("*").eq("employee_id", employee_id).execute()
    return response.data

