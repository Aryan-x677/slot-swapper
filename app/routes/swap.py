from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.utils.jwt_handler import get_current_user

router = APIRouter(
    prefix="/api",
    tags=["Swap Logic"]
)

@router.get("/swappable-slots", response_model=list[schemas.EventResponse])
def get_swappable_slots(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    slots = (
        db.query(models.Event)
        .filter(models.Event.owner_id != current_user.id)
        .filter(models.Event.status == models.EventStatus.SWAPPABLE)
        .all()
        )
    
    return slots

@router.post("/swap-request", response_model=schemas.SwapRequestResponse)
def create_swap_request(
    request_data: schemas.SwapRequestCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    my_slot = db.query(models.Event).filter(models.Event.id == request_data.my_slot_id, models.Event.owner_id == current_user.id).first()
    their_slot = db.query(models.Event).filter(models.Event.id == request_data.their_slot_id).first()

    if not my_slot or not their_slot:
        raise HTTPException(status_code=404, detail="One or both slots not found")
    
    if my_slot.status != models.EventStatus.SWAPPABLE or their_slot.status != models.EventStatus.SWAPPABLE:
        raise HTTPException(status_code=400, detail="One or both slots are not swappable")
    
    swap_request = models.SwapRequest(
        requester_id=current_user.id,
        responder_id=their_slot.owner_id,
        my_slot_id=my_slot.id,
        their_slot_id=their_slot.id,
        status=models.SwapStatus.PENDING
    )

    my_slot.status = models.EventStatus.SWAP_PENDING
    their_slot.status = models.EventStatus.SWAP_PENDING

    db.add(swap_request)
    db.commit()
    db.refresh(swap_request)

    return swap_request
    
@router.post("/swap-response/{request_id}")
def respond_to_swap_request(
    request_id: int,
    response: schemas.SwapResponseAction,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    swap_request = db.query(models.SwapRequest).filter(models.SwapRequest.id == request_id).first()

    if not swap_request:
        raise HTTPException(status_code=404, detail="Swap request not found")
    
    if swap_request.responder_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to respond to this swap request")
    
    my_slot = db.query(models.Event).filter(models.Event.id == swap_request.my_slot_id).first()
    their_slot = db.query(models.Event).filter(models.Event.id == swap_request.their_slot_id).first()

    if not my_slot or not their_slot:
        raise HTTPException(status_code=404, detail="One or both slots not found")
    
    if not response.accepted:
        swap_request.status = models.SwapStatus.REJECTED
        my_slot.status = models.EventStatus.SWAPPABLE
        their_slot.status = models.EventStatus.SWAPPABLE
        db.commit()
        return {"detail": "Swap request rejected"}
    else:
        swap_request.status = models.SwapStatus.ACCEPTED
        my_slot.owner_id, their_slot.owner_id = their_slot.owner_id, my_slot.owner_id

        my_slot.status = models.EventStatus.BUSY
        their_slot.status = models.EventStatus.BUSY

        db.commit()
        return {"detail": "Swap request accepted and slots swapped", "status": swap_request.status}

@router.get("/my-swap-requests", response_model=list[schemas.SwapRequestResponse])
def get_my_swap_requests(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    requests = db.query(models.SwapRequest).filter(
        (models.SwapRequest.requester_id == current_user.id)
    ).all()

    if not requests:
        raise HTTPException(status_code=404, detail="No swap requests found")
    
    return requests
