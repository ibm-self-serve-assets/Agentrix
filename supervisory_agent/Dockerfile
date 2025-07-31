# FROM python:3.12-slim-bookworm

# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# # Copy the project into the image
# ADD . /app

# # Sync the project into a new environment, using the frozen lockfile
# WORKDIR /app
# RUN uv sync --frozen

# CMD ["uv", "run", "main.py"]



FROM python:3.11-slim-bookworm

# Set working directory inside the container
WORKDIR /app

# Copy the project files including requirements.txt
COPY . /app

# Install system dependencies (if needed) and Python requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set the default command to run your app
CMD ["python3.11", "main.py"]
