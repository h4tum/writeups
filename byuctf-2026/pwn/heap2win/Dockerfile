FROM fedora:42

RUN dnf install -y socat libstdc++ && dnf clean all

COPY heap2win /heap2win
RUN chmod +x /heap2win

EXPOSE 9001
CMD ["socat", "TCP-LISTEN:9001,reuseaddr,fork", "EXEC:/heap2win,stderr"]
