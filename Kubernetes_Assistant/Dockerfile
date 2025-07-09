FROM python:3.11-slim
LABEL maintainer="Anand Awasthi (anand.awasthi@in.ibm.com)"

# Create a non-root user
RUN groupadd -r kubeuser && useradd -r -g kubeuser kubeuser

# Set up app directory
WORKDIR /app

# Install dependencies first (leverage Docker cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and resources
COPY kube-assistant.py .
COPY forms.py .
COPY k8scluster.py .
COPY pyproject.toml .
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
COPY .env .

# Optional: copy env_sample as .env if you want a default
#COPY env_sample .env

# Set permissions
RUN chmod -R 775 /app && chown -R kubeuser:kubeuser /app \
    && mkdir -p /home/kubeuser && chown -R kubeuser:kubeuser /home/kubeuser

USER kubeuser
EXPOSE 8080

CMD ["python", "kube-assistant.py"]
