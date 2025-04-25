FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

# Зависимости для драйвера
RUN apt-get update && apt-get install -y \
    python3-distutils \
    wget \
    gnupg \
    unzip \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    libdrm2 \
    libgbm1 \
    libxshmfence1 \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install setuptools
RUN pip install undetected-chromedriver

RUN chmod -R 777 /tmp
RUN apt-get update && apt-get install -y postgresql-client

COPY ./src src

#CMD python main.py