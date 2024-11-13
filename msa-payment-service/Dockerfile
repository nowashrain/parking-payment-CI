FROM python:3.10.15-slim-bullseye

WORKDIR /app

## 필요한 패키지 최소 설치
#RUN apt-get update && apt-get install -y --no-install-recommends \
#    build-essential \
#    liblapack-dev \
#    libblas-dev \
#    libffi-dev \
#    && rm -rf /var/lib/apt/lists/*
#
## requirements.txt 파일 복사 및 종속성 설치
#COPY requirements.txt .
#RUN pip install --upgrade pip \
#    && pip install --no-cache-dir -r requirements.txt


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# 애플리케이션 코드 복사
COPY main.py .
COPY models ./models
COPY schema ./schema
COPY routes ./routes
COPY service ./service

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
