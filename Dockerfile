FROM python:3.14-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py analysis.py setup.py ./
COPY templates ./templates
COPY static ./static
RUN useradd -m appuser && mkdir -p /data && chown -R appuser:appuser /app /data
USER appuser
ENV HOST=0.0.0.0 PORT=8765 CLASSPULSE_DATA=/data
EXPOSE 8765
CMD ["python", "app.py"]
