FROM python:3-alpine

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache gcc musl-dev postgresql-dev

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app app
COPY wsgi.py .

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]