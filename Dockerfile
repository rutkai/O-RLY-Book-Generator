FROM ubuntu

RUN set -x \
    && DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y git python-setuptools libmemcached-dev libjpeg-dev libfreetype6-dev libpq-dev build-essential libpython-dev

RUN easy_install pip

RUN git clone https://github.com/shoudusse/O-RLY-Book-Generator.git

WORKDIR O-RLY-Book-Generator

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python run.py
