FROM ubuntu:latest

RUN apt-get update \
    && apt-get install -y nodejs npm \
    && apt-get install -y \
        python3 \
        python3-pip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install markdown

RUN mkdir online_chat_messenger
