FROM python:latest

COPY . /app
WORKDIR /app

RUN adduser webapp && chown -R webapp:webapp /app

RUN apt update -y && apt install -y python3-pip \ 
    python3-dev \ 
    build-essential \
   && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt \
    && rm requirements.txt \
    && rm -rf __pycache__

EXPOSE 3000

USER webapp 

ENTRYPOINT ["python"]

CMD ["app.py"]