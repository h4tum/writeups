FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir pycryptodome

COPY server.py /app/server.py
COPY private.py /app/private.py

RUN python3 - <<'PY'
from Crypto.PublicKey import RSA
key = RSA.generate(2048)
with open('/app/private_key.pem', 'wb') as f:
    f.write(key.export_key())
PY

EXPOSE 1337

WORKDIR /app

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python3 /app/server.py"]