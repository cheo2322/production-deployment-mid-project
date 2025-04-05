FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app/app.py", "--host=0.0.0.0", "--port=5001"]