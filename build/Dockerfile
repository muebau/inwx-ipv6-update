FROM alpine:latest

RUN apk -U upgrade && apk add --no-cache python3 py3-pip bind-tools && pip install inwx-domrobot

RUN echo "*       *       *       *       *       run-parts /etc/periodic/1min" >> /etc/crontabs/root

COPY checkip /etc/periodic/1min/checkip
COPY ipupdate.py /

RUN chmod a+x /etc/periodic/1min/checkip

CMD [ "crond", "-f", "-l", "8" ]
