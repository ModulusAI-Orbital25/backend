FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install -y \
    ca-certificates \
    build-essential \
    git \
    curl \
    libffi-dev \
    libopenblas-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Pre-download huggingface model
COPY download_model.py .
RUN python download_model.py

COPY src/ .

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
	ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local /usr/local

COPY --from=builder /root/.cache/huggingface /root/.cache/huggingface

COPY --from=builder /app /app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
