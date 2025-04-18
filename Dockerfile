FROM python:3.12-slim

USER root

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    wget \
    git \
    libnss3 \
    libatk1.0-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip pipenv

# RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt --timeout=100 --index-url https://pypi.org/simple

EXPOSE 8501

# CMD ["streamlit", "run", "/app/src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
CMD ["bash", "-c", "cd /app/src && streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]