FROM python:3.8-buster

RUN useradd -ms /bin/bash vscode

# Install chrome for pytest

RUN mkdir -p /tmp/chrome \
   && cd /tmp/chrome \
   && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

RUN cd /tmp/chrome \
   && ls \
   && dpkg -i google-chrome*.deb || true \
   && apt update \
   && apt --fix-broken install -y

# Install chromedriver

RUN mkdir -p /tmp/ && \
    cd /tmp/ && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip  && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/bin/ && \
    # clean up the container "layer", after we are done
    rm /tmp/chromedriver.zip

USER vscode

ENV PATH="/home/vscode/.local/bin:${PATH}"
