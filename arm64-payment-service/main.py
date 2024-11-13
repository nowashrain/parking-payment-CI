import uvicorn, os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from routes.payment import router as payment_router
from service.database import create_tables, SessionLocal

app = FastAPI()

# CORS 설정
# origins = [
#     "http://localhost:3000",  # 허용할 프론트엔드 도메인
#     "http://127.0.0.1:3000"
# ]

origins = os.getenv("CORS_ORIGINS", 'http://localhost:3000').split(',')
print('CORS -> ', origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.on_event("startup")
def startup_event():
    create_tables()  # 애플리케이션 시작 시 테이블 생성

@app.get('/mariadb')
def mariadb():
    try:
        with SessionLocal() as conn:
            result = conn.execute(text('SELECT SYSDATE();')).scalar()
            return {'msg': 'Database Connection Successful!!', 'result': f'{result}'}
    except Exception as ex:
        return {'msg': 'Database Connection Failed!!', 'error': str(ex)}


app.include_router(payment_router)

if __name__ == "__main__":
    create_tables()
    uvicorn.run('main:app', port=8001, reload=True)



