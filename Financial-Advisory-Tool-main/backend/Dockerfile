FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    git \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group with fixed UID/GID (avoids permission conflicts)
RUN groupadd -g 1001 appuser && useradd -u 1001 -g appuser -m -d /app appuser

# Set working directory and copy files with correct ownership
WORKDIR /app
COPY --chown=appuser:appuser . .

# Install Python dependencies as root (pip cache remains owned by root)
RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

# Create and set permissions for critical directories
RUN mkdir -p /app/.local && chown -R appuser:appuser /app/.local

# Set environment variables for Python and Streamlit
ENV HOME=/app
ENV PATH="/app/.local/bin:${PATH}"

# Switch to the non-root user
USER appuser

# Expose the port FastAPI will run on
EXPOSE 8087

# Command to run the application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8087"]