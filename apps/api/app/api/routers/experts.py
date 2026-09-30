from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.models import ExpertRequest, ExpertAnswer
from app.schemas.schemas import ExpertRequestCreate, ExpertAnswerCreate

router = APIRouter(prefix="/experts", tags=["Expert Consultation Hub"])

@router.get("/requests")
async def list_expert_requests(db: AsyncSession = Depends(get_db)):
    return [
        {
            "id": "exp-req-1",
            "farmer_id": "demo-farmer-id",
            "farmer_name": "Ramanathan Farmers",
            "crop_name": "Tomato",
            "image_url": "https://images.unsplash.com/photo-1592417817098-8f3d6eb1626f?q=80&w=800&auto=format&fit=crop",
            "question": "Lower leaf spots spreading rapidly after 2 days of rain. Is this early blight or bacterial spot?",
            "status": "Answered",
            "created_at": "2026-09-26T14:20:00Z",
            "answers": [
                {
                    "id": "exp-ans-1",
                    "expert_name": "Dr. K. Swaminathan (Senior Pathologist, TNAU)",
                    "response_text": "This exhibits classic late blight water-soaked lesions rather than bacterial speck pinholes. Apply Copper Hydroxide spray at 2.0g/L immediately.",
                    "recommended_action": "Avoid overhead watering and prune lowest 15cm leaves touching soil.",
                    "created_at": "2026-09-26T16:05:00Z"
                }
            ]
        }
    ]

@router.post("/requests")
async def create_expert_request(req: ExpertRequestCreate, db: AsyncSession = Depends(get_db)):
    new_req = ExpertRequest(
        farmer_id="demo-farmer-id",
        crop_name=req.crop_name,
        image_url=req.image_url,
        question=req.question,
        status="Open"
    )
    db.add(new_req)
    await db.commit()
    await db.refresh(new_req)
    return new_req

@router.post("/answers")
async def create_expert_answer(ans: ExpertAnswerCreate, db: AsyncSession = Depends(get_db)):
    new_ans = ExpertAnswer(
        request_id=ans.request_id,
        expert_name="Dr. K. Swaminathan (Senior Pathologist)",
        response_text=ans.response_text,
        recommended_action=ans.recommended_action
    )
    db.add(new_ans)
    await db.commit()
    return {"message": "Answer recorded successfully"}
