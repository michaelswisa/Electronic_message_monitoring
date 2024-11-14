FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV POSTGRES_USER=michael
ENV POSTGRES_PASSWORD=1234
ENV POSTGRES_DB=explos_db
CMD ["python", "hostage_consumer.py"]