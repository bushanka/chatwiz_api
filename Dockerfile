FROM python:3.11


COPY . /code
RUN chmod 700 code
WORKDIR code

RUN pip install -r requirements.txt