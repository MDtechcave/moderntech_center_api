from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import employees, attendance, payroll, reviews
from app.routes import dashboard

app = FastAPI(title="StaffSync API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])
app.include_router(payroll.router, prefix="/payroll", tags=["Payroll"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/")
def root():
    return {"message": "StaffSync API is running"}