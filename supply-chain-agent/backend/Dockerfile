# ========== BACKEND RUNTIME ==========
FROM python:3.11-slim AS backend

# Set working directory
WORKDIR /app

# Copy backend code
COPY . .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install uvicorn fastapi ibm-watsonx-orchestrate

# Expose backend port
EXPOSE 3000

# Entrypoint
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
