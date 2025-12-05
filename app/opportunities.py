
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from . import models, schemas
from .deps import get_current_user

router = APIRouter(prefix="/opportunities", tags=["opportunities"])

@router.get("/", response_model=list[schemas.OpportunityRead])
def list_opportunities(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    items = db.query(models.Opportunity).order_by(models.Opportunity.created_at.desc()).all()
    return items

@router.post("/", response_model=schemas.OpportunityRead)
def create_opportunity(
    payload: schemas.OpportunityCreate,
    db: Session = Depends(get_db),
):
    opp = models.Opportunity(**payload.dict())
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return opp
