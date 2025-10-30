from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.utils.jwt_handler import get_current_user

router = APIRouter(
    prefix="/events",
    tags=["Events"]
)

@router.post("/", response_model=schemas.EventResponse)
def create_event(event: schemas.EventCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_event = models.Event(
        title=event.title,
        start_time=event.start_time,
        end_time=event.end_time,
        status=event.status,
        owner_id=current_user.id
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

@router.get("/", response_model=list[schemas.EventResponse])
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()

    return events

@router.get("/me", response_model=list[schemas.EventResponse])
def get_my_events(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    events = db.query(models.Event).filter(models.Event.owner_id == current_user.id).all()

    return events

@router.put("/{event_id}", response_model=schemas.EventResponse)
def update_event(event_id: int, event_update: schemas.EventUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.owner_id == current_user.id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    
    for key, value in event_update.dict(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id, models.Event.owner_id == current_user.id).first()

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    
    db.delete(event)
    db.commit()

    return {"message": "Event deleted successfully"}
                 