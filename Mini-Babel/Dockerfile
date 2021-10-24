FROM python:3.9.7-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "streamlit", "run" , "miniBabel.py"]