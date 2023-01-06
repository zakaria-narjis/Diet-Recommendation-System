# backend/Dockerfile

FROM python:3.10.8

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000","--reload"]