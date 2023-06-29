# pull python 3.9 image from docker hub
FROM python:3.9-alpine
MAINTAINER Noah Boussard <noah@akyos.com>

# define a new volume to store the application code inside the image
VOLUME /app
COPY .. /app

# set the working directory to /app
WORKDIR /app

# define env vars
ENV AKY_CLI_PATH /app
ENV AKY_CLI_RUNTIME_PATH /cwd

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r .docker/config/requirements.txt

# copy entrypoint script
COPY .docker/entrypoint.sh /usr/local/bin/aky
RUN chmod +x /usr/local/bin/aky

# Update dependencies
RUN apk update && apk upgrade

# Basic packages
RUN apk add --no-cache zip unzip curl

# Installing PHP@8.2
RUN apk add --no-cache php82 \
    php82-common \
    php82-fpm \
    php82-pdo \
    php82-opcache \
    php82-zip \
    php82-phar \
    php82-iconv \
    php82-cli \
    php82-curl \
    php82-openssl \
    php82-mbstring \
    php82-tokenizer \
    php82-fileinfo \
    php82-json \
    php82-xml \
    php82-xmlwriter \
    php82-simplexml \
    php82-dom \
    php82-pdo_mysql \
    php82-pdo_sqlite \
    php82-tokenizer \
    php82-pecl-redis

RUN ln -s /usr/bin/php82 /usr/bin/php

# Install Composer
RUN curl -sS https://getcomposer.org/installer -o composer-setup.php
RUN php composer-setup.php --install-dir=/usr/local/bin --filename=composer
RUN rm -rf composer-setup.php

# Install git
RUN apk add git

# Install yarn
RUN apk --no-cache add nodejs yarn --repository=http://dl-cdn.alpinelinux.org/alpine/edge/community

# Install MySQL
RUN apk add --update mysql mysql-client && rm -f /var/cache/apk/*

# run the command to start the application
ENTRYPOINT ["/usr/local/bin/aky"]