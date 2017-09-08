FROM cbankieratypon/python-2.7-flask
MAINTAINER hanwuji99
RUN mkdir /userservice && pip install pymongo
WORKDIR /userservice
ADD . /userservice/

EXPOSE 5000
ENTRYPOINT ["python", "app.py"]


