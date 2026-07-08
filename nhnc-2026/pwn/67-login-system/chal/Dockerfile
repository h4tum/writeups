FROM archlinux@sha256:d41d768e81cac3bede426e294ac5b2c55ed4bf697698c0f13ddd86b911f7f260

RUN pacman -Sy --noconfirm socat && \
    pacman -Scc --noconfirm

RUN useradd -m chal
RUN chown -R root:root /home/chal

COPY ./share /home/chal
RUN chmod -R 755 /home/chal

COPY ./startup.sh /home/startup.sh
RUN chmod 700 /home/startup.sh

COPY ./flag.txt /flag.txt
RUN chmod 755 /flag.txt

CMD ["/home/startup.sh"]

EXPOSE 16767
