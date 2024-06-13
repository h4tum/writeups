# docker build -t future-of-pwning-2 . && docker run -p 5000:5000 --rm -it future-of-pwning-2
FROM ubuntu:22.04

RUN apt-get update -y && apt-get install -y --no-install-recommends build-essential curl patchelf pip \
&& apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir flask

RUN curl -L https://github.com/ForwardCom/bintools/archive/779c06891cba05a97a214a23b7a63aeff25d983a.tar.gz | tar zxf -
WORKDIR bintools-779c06891cba05a97a214a23b7a63aeff25d983a
COPY remove-syscalls.patch ./
RUN patch -p1 --binary < remove-syscalls.patch && \
make -f forw.make compflags='-D_FORTIFY_SOURCE=0 -g3' && \
mkdir /app && cp forw instruction_list.csv /app

WORKDIR /app

# Your goal is to execute /flagme
ARG FLAG=GPNCTF{fake_flag}
RUN printf "#!/bin/sh\necho '$FLAG'" > /flagme && \
chmod +x /flagme

RUN cp /lib64/ld-linux-x86-64.so.2 . \
&& cp /lib/x86_64-linux-gnu/libc.so.6 . \
&& cp /lib/x86_64-linux-gnu/libstdc++.so.6 . \
&& cp /lib/x86_64-linux-gnu/libgcc_s.so.1 . \
&& cp /lib/x86_64-linux-gnu/libm.so.6 . \
&& sed -i 's;/bin/sh;/flagme;' libc.so.6  # this is for convenience, see above
RUN patchelf --set-interpreter ld-linux-x86-64.so.2 --set-rpath . ./forw

COPY app.py ./
EXPOSE 5000
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0"]
