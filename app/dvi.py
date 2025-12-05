
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from .database import get_db
from . import models, schemas
from .deps import get_current_user

router = APIRouter(prefix="/dvi", tags=["dvi"])

def _scale(x: int) -> float:
    # simple scaling 0-10 -> 0-100
    return float(x) * 10.0

@router.post("/calculate", response_model=schemas.DVIProfileRead)
def calculate_dvi(
    payload: schemas.DVICalcInput,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    financial = _scale((payload.financial_stability + payload.income_outlook) // 2)
    career = _scale(payload.career_clarity)
    skills = _scale(payload.skills_level)
    wellbeing = _scale(payload.wellbeing_status)
    integration = _scale(payload.social_integration)

    overall = (financial + career + skills + wellbeing + integration) / 5.0

    dvi = models.DVIProfile(
        user_id=user.id,
        overall_score=overall,
        financial=financial,
        career=career,
        wellbeing=wellbeing,
        integration=integration,
        skills=skills,
        created_at=datetime.utcnow(),
    )
    db.add(dvi)
    db.commit()
    db.refresh(dvi)

    return schemas.DVIProfileRead(
        id=dvi.id,
        overall_score=dvi.overall_score,
        dimensions=schemas.DVIDimensionScores(
            financial=dvi.financial,
            career=dvi.career,
            wellbeing=dvi.wellbeing,
            integration=dvi.integration,
            skills=dvi.skills,
        ),
        created_at=dvi.created_at,
    )

@router.get("/history", response_model=list[schemas.DVIProfileRead])
def get_dvi_history(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    profiles = (
        db.query(models.DVIProfile)
        .filter(models.DVIProfile.user_id == user.id)
        .order_by(models.DVIProfile.created_at.desc())
        .all()
    )
    return [
        schemas.DVIProfileRead(
            id=p.id,
            overall_score=p.overall_score,
            dimensions=schemas.DVIDimensionScores(
                financial=p.financial,
                career=p.career,
                wellbeing=p.wellbeing,
                integration=p.integration,
                skills=p.skills,
            ),
            created_at=p.created_at,
        )
        for p in profiles
    ]
