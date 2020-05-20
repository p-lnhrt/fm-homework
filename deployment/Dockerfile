FROM python:3.6.8-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

ENV FLASK_APP=predictionws
ENV FLASK_ENV=production

ENTRYPOINT ["/usr/local/bin/flask", "run"]
CMD ["--host=0.0.0.0", "--port=5000"]