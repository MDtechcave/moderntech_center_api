from fastapi import APIRouter, HTTPException
from app.database import supabase
from pydantic import BaseModel

router = APIRouter()

class ReviewInput(BaseModel):
    employee_id: int
    rating: int
    comments: str

@router.get("/")
def get_reviews():
    response = supabase.table("performance_reviews").select("*, employees(name, position)").execute()
    return response.data

@router.post("/")
def submit_review(review: ReviewInput):
    if not 1 <= review.rating <= 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    response = supabase.table("performance_reviews").insert({
        "employee_id": review.employee_id,
        "rating": review.rating,
        "comments": review.comments
    }).execute()

    return {"message": "Review submitted", "data": response.data}