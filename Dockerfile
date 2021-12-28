FROM python:3.9

COPY liquid/ /home/liquid/
COPY config.py /home
COPY requirements.txt /home
COPY init_db.py /home
WORKDIR /home

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get -y install ffmpeg libsm6 libxext6 \
    && pip install -r requirements.txt

# FLASK_ENV should be overidden during prod deployment
ENV FLASK_APP liquid
ENV FLASK_ENV development

EXPOSE 8080

ENTRYPOINT ["flask", "run", "--port", "8080", "--host=0.0.0.0"]
