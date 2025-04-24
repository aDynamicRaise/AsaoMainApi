FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка последней стабильной версии Chromium и ChromeDriver
#RUN apt-get update && \
#    apt-get install -y wget gnupg && \
#    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list && \
#    apt-get update && \
#    apt-get install -y google-chrome-stable && \
#    rm -rf /var/lib/apt/lists/*

# Установка ChromeDriver той же версии
#RUN CHROME_VERSION=$(google-chrome --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+') && \
#    wget -q https://chromedriver.storage.googleapis.com/${CHROME_VERSION}/chromedriver_linux64.zip && \
#    unzip chromedriver_linux64.zip -d /usr/bin/ && \
#    chmod +x /usr/bin/chromedriver && \
#    rm chromedriver_linux64.zip

RUN apt-get update && apt-get install -y \
    python3-distutils \
    wget \
    chromium \
    chromium-driver

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN pip install setuptools

RUN chmod -R 777 /tmp
RUN apt-get update && apt-get install -y postgresql-client

COPY ./src src

#CMD python main.py