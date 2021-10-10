FROM python:3.7.9-slim-buster
WORKDIR /code
ENV FLASK_APP=server_app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "server.py"]