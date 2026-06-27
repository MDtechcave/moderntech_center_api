from fastapi import APIRouter, HTTPException
from app.database import supabase
from pydantic import BaseModel

router = APIRouter()

class LeaveRequest(BaseModel):
    employee_id: int
    date: str
    reason: str

class LeaveStatusUpdate(BaseModel):
    status: str

@router.get("/")
def get_attendance():
    response = supabase.table("attendance").select("*, employees(name)").execute()
    return response.data

@router.get("/leave")
def get_leave_requests():
    response = supabase.table("leave_requests").select("*").execute()
    return response.data

@router.get("/leave/balance/{employee_id}")
def get_leave_balance(employee_id: int):
    response = supabase.table("leave_balances").select("*").eq("employee_id", employee_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Leave balance not found")
    return response.data[0]

@router.post("/leave")
def submit_leave(leave: LeaveRequest):
    response = supabase.table("leave_requests").insert({
        "employee_id": leave.employee_id,
        "date": leave.date,
        "reason": leave.reason,
        "status": "Pending"
    }).execute()
    return {"message": "Leave request submitted", "data": response.data}

@router.patch("/leave/{leave_id}")
def update_leave_status(leave_id: int, update: LeaveStatusUpdate):
    if update.status not in ["Approved", "Denied"]:
        raise HTTPException(status_code=400, detail="Status must be Approved or Denied")
    
    response = supabase.table("leave_requests").update({
        "status": update.status
    }).eq("id", leave_id).execute()

    return {"message": f"Leave request {update.status}", "data": response.data}

@router.get("/{employee_id}")
def get_employee_attendance(employee_id: int):
    response = supabase.table("attendance").select("*").eq("employee_id", employee_id).execute()
    return response.data