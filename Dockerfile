FROM python:3

COPY requirements.txt /

RUN groupadd -r uwsgi \
    && useradd -r -g uwsgi uwsgi \
    && pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY app /app
COPY cmd.sh /

EXPOSE 8000 9000
USER uwsgi

CMD ["/cmd.sh"]
