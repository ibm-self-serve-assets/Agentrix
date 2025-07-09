# ========== FRONTEND BUILD ==========
# ----- Frontend Stage -----
FROM node:20 AS frontend
WORKDIR /app
COPY frontend/ ./frontend
WORKDIR /app/frontend
RUN npm install
RUN npm run build
# ========== BACKEND RUNTIME ==========
# ----- Backend Stage -----
FROM python:3.11-slim AS backends

WORKDIR /app
COPY --from=frontend /app/frontend/build ./frontend/build
COPY backend/ ./backend

RUN pip install --no-cache-dir -r backend/requirements.txt


# Expose port
EXPOSE 8000

# Entrypoint
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
