from sqlalchemy.orm import Session
from models.payment import Payment, Parking
from schema.payment import PaymentBase
from datetime import datetime

# 새로운 결제 등록
def register(db: Session, payment: PaymentBase):
    new_payment = Payment(
        payment=payment.payment,
        parkingtime=payment.parkingtime,
        carnum=payment.carnum
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

# 결제 목록 조회
def paymentlist(db: Session):
    return db.query(Payment).order_by(Payment.carnum.desc()).all()

# 특정 차량 번호에 따른 결제 조회
def paymentone(db: Session, pno: int):
    print(pno)
    return db.query(Parking).filter(Parking.pno == pno).first()


