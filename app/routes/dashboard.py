from fastapi import APIRouter
from app.database import supabase
from datetime import date

router = APIRouter()

@router.get("/admin")
def get_admin_stats():
    employees = supabase.table("employees").select("*").execute().data
    attendance = supabase.table("attendance").select("*").execute().data
    leave = supabase.table("leave_requests").select("*").execute().data

    today = str(date.today())

    present_today = [a for a in attendance if a["date"] == today and a["status"] == "Present"]
    pending_leave = [l for l in leave if l["status"] == "Pending"]

    total_payroll = sum(emp["salary"] for emp in employees)

    return {
        "total_employees": len(employees),
        "present_today": len(present_today),
        "pending_leave_requests": len(pending_leave),
        "total_monthly_payroll": total_payroll
    }

@router.get("/employee/{employee_id}")
def get_employee_stats(employee_id: int):
    attendance = supabase.table("attendance").select("*").eq("employee_id", employee_id).execute().data
    leave = supabase.table("leave_requests").select("*").eq("employee_id", employee_id).execute().data
    employee = supabase.table("employees").select("*").eq("id", employee_id).execute().data

    if not employee:
        return {"error": "Employee not found"}

    emp = employee[0]
    total_days = len(attendance)
    present_days = sum(1 for a in attendance if a["status"] == "Present")
    absent_days = sum(1 for a in attendance if a["status"] == "Absent")
    approved_leave = sum(1 for l in leave if l["status"] == "Approved")
    pending_leave = sum(1 for l in leave if l["status"] == "Pending")

    total_working_days = 22
    daily_rate = emp["salary"] / total_working_days
    deduction = round(daily_rate * absent_days)
    final_salary = round(emp["salary"] - deduction)

    return {
        "name": emp["name"],
        "position": emp["position"],
        "department": emp["department"],
        "total_days": total_days,
        "present_days": present_days,
        "absent_days": absent_days,
        "approved_leave": approved_leave,
        "pending_leave": pending_leave,
        "salary": emp["salary"],
        "deduction": deduction,
        "final_salary": final_salary,
        "leave_requests": leave
    }