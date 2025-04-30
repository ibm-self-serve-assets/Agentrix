FROM python:3.10
WORKDIR /app
COPY requirements.txt .
COPY main.py .
COPY . .
RUN pip3 install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
