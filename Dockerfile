FROM python:alpine

COPY . .

RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base \
  && apk --no-cache add poppler poppler-utils poppler-dev \
  && pip install --upgrade pip \
  && pip install -r requirements.in \
  && apk del build-dependencies

ENTRYPOINT ["python", "main.py"]


