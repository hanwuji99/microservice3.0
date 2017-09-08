FROM cbankieratypon/python-2.7-flask
MAINTAINER hanwuji99
RUN mkdir /movieservice && pip install pymongo
WORKDIR /movieservice
ADD . /movieservice/

EXPOSE 5001
ENTRYPOINT ["python", "app.py"]


