# docker build -t dreamer . && docker run -p 1337:1337 -t dreamer
FROM archlinux:latest

RUN pacman -Sy --noconfirm socat gcc

WORKDIR /app

COPY  dream.c /app/
RUN gcc /app/dream.c -o dream
ARG FLAG=GPNCTF{fake_flag}
RUN echo "$FLAG" > flag.txt

EXPOSE 1337

ENTRYPOINT [ "socat", "tcp-l:1337,reuseaddr,fork", "EXEC:./dream,stderr" ]
