from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated

app = FastAPI(
    title="Content Moderation Platform API",
    description="API for submitting and moderating content in real-time.",
    version="0.1.0"
)

# Defining the request body model
class ContentSubmission(BaseModel):
    """Represents piece of content submitted by a user."""
    user_id: int
    text: str

# User auth function
# This could check a token or session
# For now, we will simulate a logged in user
async def get_current_user():
    """Placeholder dependency for user auth"""
    # Hardcoded for now, to be replaced with JWT token validation later
    return {"user_id": 123, "username": "testuser"}

@app.post("/submit/", status_code=status.HTTP_202_ACCEPTED)
async def submit_content(
    submission: ContentSubmission,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    """
    Accepts text content for moderation.

    - Validates the input against the ContentSubmission mode.
    - Simulates user auth.
    - For now, it just returns a confirmation.
    """
    print(f"Received submissin from user_id: {submission.user_id}")
    print(f"Content: {submission.text}")

    return {
        "message": "Content received and queued for moderation.",
        "submission_data": submission
    }

@app.get("/")
def read_root():
    return {"status": "Moderation API is running"}