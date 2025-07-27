FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    ca-certificates \            # ← add this
    build-essential \
    git \
    curl \
    libffi-dev \
    libopenblas-dev \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["flask", "--app", "src/app", "run", "--host=0.0.0.0"]

# CMD ["pytest"]
