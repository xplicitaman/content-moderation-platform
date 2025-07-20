from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal, engine
import models

import pika
import json

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

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
        await db.commit()

@app.post("/submit/", status_code=status.HTTP_202_ACCEPTED)
async def submit_content(
    submission: ContentSubmission,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Accepts text content for moderation.

    - Validates the input against the ContentSubmission model.
    - Simulates user auth.
    - For now, it just returns a confirmation.
    """
    print(f"Received submissin from user_id: {submission.user_id}")
    print(f"Content: {submission.text}")
    
    new_submission = models.Submission(
        user_id=submission.user_id,
        text=submission.text,
        status="pending"
    )
    db.add(new_submission)
    await db.flush()

    connection_parameters = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='moderation_queue')

    message_body = {
        "submission_id": new_submission.id,
        "text": new_submission.text
    }

    channel.basic_publish(
        exchange='',
        routing_key='moderation_queue',
        body=json.dumps(message_body)
    )
    connection.close()

    print(f"[*] Publised moderation job for submission_id: {new_submission.id}")

    return {
        "message": "Content received and queued for moderation.",
        "submission_data": new_submission.id
    }

@app.get("/")
def read_root():
    return {"status": "Moderation API is running"}