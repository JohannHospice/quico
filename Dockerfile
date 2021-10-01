FROM python:3.7-alpine

WORKDIR /app

COPY ./src ./install.sh ./

RUN chmod +x ./install.sh \
    && ./install.sh

ENTRYPOINT [ "quico" ]
