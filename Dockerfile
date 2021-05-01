# By jackmwhit

FROM python:3.8-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Please enter your server token, the name of the channel you want monitored, the channel's id, and the role name for the bet moderators
ENV TOKEN=
ENV CHANNELID=
ENV BETMOD=

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "main.py"]