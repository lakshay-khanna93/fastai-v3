FROM python:3.8-slim-buster

RUN apt-get update && apt-get install -y git python3-dev gcc \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .

RUN pip install --upgrade -r requirements.txt

COPY app app/

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential gcc \
                                        libsndfile1
RUN python app/server.py

EXPOSE 5000

CMD ["python", "app/server.py", "serve"]
