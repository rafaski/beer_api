FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app

RUN apt-get install libpq-dev

RUN pip3 install --upgrade setuptools \
    && pip3 install --upgrade pip \
    && pip install -r requirements.txt

COPY . /app

#
#CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8080"]