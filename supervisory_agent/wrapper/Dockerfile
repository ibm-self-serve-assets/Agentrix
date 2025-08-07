FROM python:3.11-slim

# Set working directory to /wrapper
WORKDIR /wrapper

# Copy only what's needed
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code and env
COPY . .

# Default command
CMD ["python", "api.py"]
