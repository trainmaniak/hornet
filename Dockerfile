FROM balenalib/rpi-raspbian

RUN apt update && apt install -y python3 python3-venv python3-pip iputils-ping ssh

RUN mkdir /opt/cerebro
COPY app /opt/cerebro/
COPY docker-entrypoint.sh /opt/cerebro/
RUN chmod +x /opt/cerebro/docker-entrypoint.sh

RUN /bin/bash -c 'cd /opt/cerebro/ && python3 -m venv venv && source venv/bin/activate && pip3 install -r requirements.txt'

CMD ["/opt/cerebro/docker-entrypoint.sh"]
