# FROM python:3.9-slim

# WORKDIR /app

# COPY . /app

# # Upgrade pip and install numpy first
# RUN pip install --upgrade pip setuptools wheel
# RUN pip install --upgrade numpy

# RUN pip install -r requirements.txt
# ENV FLASK_ENV production

# EXPOSE 3001

# CMD ["python", "-u", "./app/main.py"]



FROM python:3.12-slim

WORKDIR /app

COPY . /app

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install requirements while allowing dependency resolution
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV production

EXPOSE 3001

CMD ["python", "-u", "./app/main.py"]
