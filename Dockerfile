FROM ubuntu:latest
MAINTAINER k_kanou

RUN apt-get update \
  && apt-get install python3 python3-pip curl git sudo cron -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt
RUN git clone https://github.com/taku910/mecab.git
WORKDIR /opt/mecab/mecab
RUN ./configure  --enable-utf8-only \
  && make \
  && make check \
  && make install \
  && ldconfig

WORKDIR /opt/mecab/mecab-ipadic
RUN ./configure --with-charset=utf8 \
  && make \
  && make install

WORKDIR /opt
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
WORKDIR /opt/mecab-ipadic-neologd
RUN ./bin/install-mecab-ipadic-neologd -n -y

# Add our code
ADD ./webapp /opt/webapp/
WORKDIR /opt/webapp

# Install dependencies
ADD ./webapp/requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -qr /tmp/requirements.txt

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku			
CMD gunicorn --bind 0.0.0.0:$PORT wsgi
