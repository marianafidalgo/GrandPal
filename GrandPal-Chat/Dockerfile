FROM python:3.7.9-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "streamlit", "run" , "grandpal-chat.py"]
