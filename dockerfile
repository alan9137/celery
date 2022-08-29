FROM python
WORKDIR /project

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV HOST 0.0.0.0

ENV BROKER_REDIS_URL redis://cache:6379/0

ENV BACKEND_REDIS_URL redis://cache:6379/0

EXPOSE 5000

VOLUME [ "/project" ]
