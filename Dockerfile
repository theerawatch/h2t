# Dockerfile, Image Container
FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update \
    && apt-get -y install tesseract-ocr \
    tesseract-ocr-eng \
    libsm6 \
    libxrender1 \
    libfontconfig1 \
    libice6 \
    *libarchive13* \
    libarchive13

COPY . .

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]