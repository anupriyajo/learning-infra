FROM python:3-alpine

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app app

ENTRYPOINT ["python3", "app/server.py"]