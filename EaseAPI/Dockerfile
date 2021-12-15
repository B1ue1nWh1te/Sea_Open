FROM python:3.8-slim

WORKDIR /EaseApi

COPY ./requirements.txt .

RUN python3 -m pip config set global.index-url https://mirrors.aliyun.com/pypi/simple

RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "./Api.py"]