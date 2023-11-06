FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY api.py .

EXPOSE 8081

CMD uvicorn api:app --host 0.0.0.0 --port 8081