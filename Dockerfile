FROM python:3.11

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /code

RUN chmod 700 code

WORKDIR /code