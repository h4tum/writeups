### SET UP APP ENVIRONMENT ###
FROM ubuntu:24.04 AS app

RUN apt update

### SET UP JAIL ENVIRONMENT ###
FROM pwn.red/jail
COPY --from=app / /srv

# copy challenge file over
COPY angr_management /srv/app/run

# setup jail
ENV JAIL_TIME=900 JAIL_MEM=50M JAIL_CONNS_PER_IP=10 JAIL_CPU=1000
