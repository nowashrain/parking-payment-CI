from datetime import datetime

from pydantic import BaseModel
from typing import Optional

# 결제 기본 정보 스키마
class PaymentBase(BaseModel):
    payment: str
    parkingtime: str
    carnum: str

    class Config:
        from_attributes = True  # orm_mode 대신 사용

# 새로운 결제 생성 시 필요한 필드를 상속
class PaymentCreate(PaymentBase):
    pass

# 결제 조회 시 사용되는 스키마
class Payment(PaymentBase):
    payid: int

# 결제 목록 조회 시 사용되는 스키마
class PaymentList(BaseModel):
    payment: str
    paydate: str
    parkingtime: str
    carnum: str

    class Config:
        from_attributes = True  # orm_mode 대신 사용

class CarNumRequest(BaseModel):
    carnum: str

class ParkingList(BaseModel):
    pno: int
    carnum: str
    barrier: str
    intime: datetime
    outtime: datetime

    class Config:
        from_attributes = True  # orm_mode 대신 사용