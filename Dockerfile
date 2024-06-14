FROM python:3.12.4-alpine
WORKDIR /app
EXPOSE 8000
ENV PYTHONPATH "." 
COPY requirements.txt /app
COPY crontab /etc/cronjob
RUN apk add --no-cache gcc=13.2.1_git20240309-r0 musl-dev=1.2.5-r0 \
    libffi-dev=3.4.6-r0 && \
    pip install --no-cache-dir -r requirements.txt && \
    python -c 'import uuid; print(f"LICHESS_CLIENT_ID=\"{uuid.uuid4()}\"")' >> .env && \
    python -c 'import secrets; print(f"SECRET_KEY=\"{secrets.token_hex()}\"")' >> .env
COPY . /app
RUN flask create-db
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "src.run:app"]
