FROM pwn.red/jail

COPY --from=ubuntu / /srv

WORKDIR /srv/app/

COPY src/flag.txt .
COPY src/intro run

ENV JAIL_TIME=60 JAIL_MEM=20M JAIL_CONNS_PER_IP=10
