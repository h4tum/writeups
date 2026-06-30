FROM --platform=linux/amd64 alpine:3.20 AS readflag

RUN apk add --no-cache gcc musl-dev python3
WORKDIR /src
COPY src/readflag.c /src/readflag.c
COPY flag.txt /src/flag.txt
RUN python3 -c 'from pathlib import Path; src = Path("/src/readflag.c").read_text(); flag = Path("/src/flag.txt").read_text().rstrip("\n"); Path("/src/readflag_patched.c").write_text(src.replace("SEKAI{REPLACE_ME}", flag))' \
    && gcc /src/readflag_patched.c -static -O2 -s -o /readflag \
    && chmod 4511 /readflag

FROM ubuntu:20.04 AS app

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential autoconf automake libtool pkg-config m4 git \
        libssl-dev zlib1g-dev libcurl4-openssl-dev \
        socat ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

ENV CFG="--enable-shared --disable-static --prefix=/usr/local"
RUN git clone https://github.com/libimobiledevice/libplist && \
    cd libplist && git checkout 32428abacb909988e8e960a8845a6430b17b6a60 && \
    ./autogen.sh --without-cython $CFG && make -j"$(nproc)" && make install

RUN git clone https://github.com/libimobiledevice/libimobiledevice-glue && \
    cd libimobiledevice-glue && git checkout da770a7687f35fbb981db4d7b47b1b032cd5c2c7 && \
    ./autogen.sh $CFG && make -j"$(nproc)" && make install

RUN git clone https://github.com/libimobiledevice/libusbmuxd && \
    cd libusbmuxd && git checkout 93eb168bf6b07472d17781328c21df0c60300524 && \
    ./autogen.sh $CFG && make -j"$(nproc)" && make install

RUN git clone https://github.com/libimobiledevice/libtatsu && \
    cd libtatsu && ./autogen.sh $CFG && make -j"$(nproc)" && make install

RUN git clone https://github.com/libimobiledevice/libimobiledevice && \
    cd libimobiledevice && git checkout fa0f79190142bc309307967c058f89c1b36eb6b8 && \
    ./autogen.sh --without-cython $CFG && make -j"$(nproc)" && make install

RUN echo /usr/local/lib > /etc/ld.so.conf.d/local.conf && ldconfig

COPY src/afc_list.c /build/afc_list.c
RUN mkdir -p /app && \
    gcc -O0 -fstack-protector-all -no-pie -o /app/afc_list /build/afc_list.c \
        $(pkg-config --cflags --libs libimobiledevice-1.0) -lpthread

COPY --from=readflag /readflag /readflag

# nsjail uses one-way pipes; socat gives afc_list a bidirectional fd 0
RUN printf '#!/bin/sh\nexec socat STDIO EXEC:/app/afc_list\n' > /app/run

RUN useradd -m ctf \
    && chmod 755 /app/afc_list /app/run \
    && chown ctf:ctf /app/afc_list /app/run \
    && chown root:root /readflag \
    && chmod 4511 /readflag

FROM ghcr.io/es3n1n/jail:latest

COPY --from=app / /srv
COPY hook.sh /jail/hook.sh
RUN chown root:root /srv/readflag \
    && chmod 4511 /srv/readflag

ENV JAIL_PORT=5000 \
    JAIL_TIME=120 \
    JAIL_MEM=256M \
    JAIL_CPU=1000 \
    JAIL_PIDS=16 \
    JAIL_TMP_SIZE=0 \
    JAIL_SYSCALLS=personality
