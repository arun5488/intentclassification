FROM python:3.12.11-slim
WORKDIR /app
COPY . .
RUN apt update -y && apt install awscli -y

RUN apt-get update && pip install -r requirements.txt
CMD ["python", "app.py"]