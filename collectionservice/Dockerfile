FROM cbankieratypon/python-2.7-flask
MAINTAINER hanwuji99
RUN mkdir /collectionservice && pip install pymongo
#&& pip install redis
WORKDIR /collectionservice
ADD . /collectionservice/

EXPOSE 5004
ENTRYPOINT ["python", "app.py"]


