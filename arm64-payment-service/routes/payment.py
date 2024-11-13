
from typing import Optional, List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from schema.payment import PaymentBase, Payment, PaymentList, CarNumRequest, ParkingList, PaymentCreate
from service.database import get_db
from service.payment import register, paymentlist, paymentone

router = APIRouter()



# 정산내역 (리스트 형식)
@router.get('/paycheck', response_model=list[PaymentList])
async def paycheck(db: Session = Depends(get_db)):
    paycheck = paymentlist(db)
    return [PaymentList.model_validate(p) for p in paycheck]


# 특정 정산내역
@router.get('/payment/{pno:int}')
async def get_paymentone(pno: int, db: Session = Depends(get_db)):
    parkings = paymentone(db, pno)
    if not parkings:
        raise HTTPException(404, '결제내역이 없습니다')
    return ParkingList.model_validate(parkings)

# @router.post('/payment/complete')
# async def complete_payment(payment_data: PaymentBase, db: Session = Depends(get_db)):
#     try:
#         new_payment = Payment(
#             payment=payment_data.payment,
#             paydate=payment_data.paydate,
#             parkingtime=payment_data.parkingtime,
#             carnum=payment_data.carnum
#         )
#         db.add(new_payment)
#         db.commit()
#         db.refresh(new_payment)
#         return {"status": "success", "message": "형식적으로 결제가 완료되었습니다."}
#     except Exception as e:
#         db.rollback()
#         print("Error:", str(e))
#         raise HTTPException(status_code=500, detail="Failed to register payment: " + str(e))

@router.post('/payment/complete')
async def complete_payment(payment_data: PaymentBase, db: Session = Depends(get_db)):
    try:
        new_payment = register(db, payment_data)
        return {"status": "success", "message": "결제가 완료되었습니다.", "data": new_payment}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to register payment: {e}")
