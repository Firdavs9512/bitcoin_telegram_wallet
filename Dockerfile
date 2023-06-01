FROM python:3.10
WORKDIR /bot
COPY requirements.txt /bot/
RUN apt install -y postgresql postgresql-contrib mysql-server libpq-dev libmysqlclient-dev
RUN apt install build-essential python3-dev libgmp3-dev libssl-dev
RUN pip install -r requirements.txt
COPY . /bot
CMD python bot.py
