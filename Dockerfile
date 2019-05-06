FROM labhackercd/alpine-python3-nodejs

ENV BUILD_PACKAGES python3 python3-dev linux-headers curl curl-dev \
    git ca-certificates gcc postgresql-dev build-base bash \
    postgresql-client gettext libxml2-dev libxslt-dev zlib-dev jpeg-dev

RUN apk add --update --no-cache $BUILD_PACKAGES

ADD . /var/labhacker/edemocracia
WORKDIR /var/labhacker/edemocracia

RUN pip install -U pipenv psycopg2 gunicorn
RUN pipenv install --system

RUN npm install && \
    npm rebuild node-sass --force

RUN python3 src/manage.py build_mkdocs && \
    python3 src/manage.py collectstatic --no-input && \
    python3 src/manage.py compilemessages

RUN python3 src/manage.py makemigrations auth

EXPOSE 8000
CMD ["python3", "src/manage.py", "runserver", "0.0.0.0:8000"]