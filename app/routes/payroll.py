from fastapi import APIRouter
from app.database import supabase

router = APIRouter()

@router.get("/")
def get_payroll():
    employees = supabase.table("employees").select("*").execute().data
    attendance = supabase.table("attendance").select("*").execute().data
    leave = supabase.table("leave_requests").select("*").eq("status", "Approved").execute().data

    payslips = []

    for emp in employees:
        emp_attendance = [a for a in attendance if a["employee_id"] == emp["id"]]
        emp_leave = [lv for lv in leave if lv["employee_id"] == emp["id"]]

        total_days = 22
        present_days = sum(1 for a in emp_attendance if a["status"] == "Present")
        approved_leave = len(emp_leave)
        absent_days = sum(1 for a in emp_attendance if a["status"] == "Absent")

        daily_rate = emp["salary"] / total_days
        deduction = round(daily_rate * absent_days)
        final_salary = round(emp["salary"] - deduction)

        payslips.append({
            "employee_id": emp["id"],
            "name": emp["name"],
            "position": emp["position"],
            "department": emp["department"],
            "contact": emp["contact"],
            "salary": emp["salary"],
            "total_days": total_days,
            "present_days": present_days,
            "approved_leave": approved_leave,
            "absent_days": absent_days,
            "deduction": deduction,
            "final_salary": final_salary
        })

    return payslips