FROM python:3.9-slim

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN pip3 install -r /app/requirements.txt

ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]
