FROM python:3.12
 
 WORKDIR /app
 
 ENV PYTHONDONTWRITEBYTECODE 1
 ENV PYTHONUNBUFFERED 1
 
 COPY requirements.txt requirements.txt
 
 RUN pip install --no-cache-dir --upgrade -r requirements.txt
 
 RUN apt-get update && apt-get install -y postgresql-client
 
 COPY ./src src

#CMD python main.py