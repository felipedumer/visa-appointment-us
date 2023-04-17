FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

# RUN apt update && apt install -y wget && apt install -y chromium
RUN pip3 install -r requirements.txt
# RUN wget https://dl-ssl.google.com/linux/linux_signing_key.pub -O /tmp/google.pub
# RUN gpg --no-default-keyring --keyring /etc/apt/keyrings/google-chrome.gpg --import /tmp/google.pub
# RUN echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
# RUN apt update && apt install -y google-chrome-stable


COPY . .

CMD [ "python", "visa.py"]