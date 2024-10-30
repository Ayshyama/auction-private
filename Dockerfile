# use python 3.11 on a slim debian-based image
FROM python:3.11-slim

# install npm
RUN apt-get update && \
    apt-get install -y npm poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt /app/
RUN pip install -r /app/requirements.txt

# set working-dir and copy project files
COPY . /app
WORKDIR /app

# create static files and media dir
RUN mkdir -p /var/www/auction-private/static /var/www/auction-private/media

# copy default media files
COPY media /var/www/auction-private/media

# create non-root user and adjust permissions
RUN adduser --disabled-password --gecos '' django

# change ownership of the /app, static and mediafiles dir
RUN chown -R django:django /app /var/www/auction-private/static /var/www/auction-private/media

# switch to non-root user
USER django

# set entrypoint
ENTRYPOINT ["gunicorn", "auction_private.wsgi:application", "--bind", "0.0.0.0:8001", "--timeout", "600"]

# expose port 8001
EXPOSE 8001
