FROM python:3.7

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN pip install -r /app/requirements.txt

EXPOSE 5000
CMD ["python", "/app/flask_app.py", "--host=0.0.0.0"]
