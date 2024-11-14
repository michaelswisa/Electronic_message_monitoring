FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY messages_all_consumer.py .
CMD ["python", "messages_all_consumer.py"]
