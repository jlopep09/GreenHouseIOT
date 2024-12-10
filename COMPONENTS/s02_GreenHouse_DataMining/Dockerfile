FROM python:3.13 AS builder


WORKDIR /code/app


COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt


COPY ./app /code/app

CMD ["reflex", "run", "--loglevel", "debug"]
#CMD ["reflex", "run"]