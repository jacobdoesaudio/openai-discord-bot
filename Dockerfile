# Dockerfile, Image, Container
FROM python:latest

WORKDIR /app

COPY requirements.txt .

ADD main.py .
ADD ask_openai.py .

RUN pip install -r requirements.txt

CMD ["python", "./main.py" ]