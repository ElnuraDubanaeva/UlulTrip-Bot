FROM python:3.10

EXPOSE 4489

RUN mkdir -p /opt/services/ggeek_bot
WORKDIR /opt/services/ggeek_bot

RUN mkdir -p /opt/services/geektech-back/requirements
ADD requirements.txt opt/services/ggeek_bot/
COPY . /opt/services/ggeek_bot/

RUN pip install -r requirements.txt
CMD ["python","/opt/services/ggeek_bot/main.py"]





