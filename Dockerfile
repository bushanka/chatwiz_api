FROM python:3.11

COPY . /code
RUN chmod 700 code
WORKDIR /code
ENV PATH="/usr/src/app:${PATH}"

RUN pip install -r requirements.txt