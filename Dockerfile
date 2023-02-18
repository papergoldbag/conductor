FROM python:3.11

RUN mkdir /conductor
WORKDIR /conductor
COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "conductor.core.asgi:app", "--host=127.0.0.1", "--port=8080", "--workers=1"]
