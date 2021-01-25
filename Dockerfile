FROM python:alpine

COPY . .

RUN apk add --update --no-cache build-base python3-dev python3 libffi-dev libressl-dev bash git gettext curl \
    && curl -O https://bootstrap.pypa.io/get-pip.py \
    && python3 get-pip.py \
    && pip install --upgrade six awscli awsebcli

RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev py-pip build-base \
    && apk --no-cache add poppler poppler-utils poppler-dev \
    && pip3 install --upgrade pip \
    && pip3 install pdftotext faker nltk \    
    && apk del build-dependencies

RUN python3 -c "import nltk;dler = nltk.downloader.Downloader();dler._update_index();dler.download('punkt')"

# WORKDIR /app
ENTRYPOINT [ "python3", "main.py"]
# ENTRYPOINT ["tail", "-f", "/dev/null"]