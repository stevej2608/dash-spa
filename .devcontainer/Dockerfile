FROM python:3.8-buster

RUN useradd -ms /bin/bash vscode

# RUN apt-get update && apt-get install -y build-essential g++ libx11-dev libxkbfile-dev libsecret-1-dev

USER vscode

ENV PATH="/home/vscode/.local/bin:${PATH}"
