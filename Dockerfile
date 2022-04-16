FROM ubuntu:latest
WORKDIR /app
ADD . /app
RUN set -xe \
    && apt-get update && apt-get install -y \
    && apt-get install -y python3-pip
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    gcc \
    libc-dev \
    libffi-dev


RUN pip install wheel hdwallet
RUN pip install bip_utils apscheduler python-dotenv


RUN git clone https://github.com/artmalini/BTCBreaker.git btcbreaker


ENTRYPOINT ["python3", "./app.py"]