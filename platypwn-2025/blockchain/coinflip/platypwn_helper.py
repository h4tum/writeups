
import pwn
import time

def kill_instance(spawner):
    r = pwn.remote(*spawner)
    r.recvuntil(b"action? ")
    r.sendline(b"2")
    r.recvline()
    resp = r.recvline()
    assert b'killed' in resp

def spawn_instance(spawner):
    while True:
        r = pwn.remote(*spawner)
        r.recvuntil(b"action? ")
        r.sendline(b"1")

        r.recvline()
        resp = r.recvline()
        if b"deploying" in resp:
            r.recvuntil(b"information\r\n")
            break

        r.close()
        time.sleep(3)
        kill_instance(spawner)
        time.sleep(3)

    uuid = r.recvline().split()[-1]
    rpc = r.recvline().split()[-1].decode()
    privatekey = r.recvline().split()[-1].decode()
    address = r.recvline().split()[-1].decode()
    setupAddress = r.recvline().split()[-1].decode()

    return {
        "RPC" : rpc,
        "PrivateKey" : privatekey,
        "Address" : address,
        "setupAddress": setupAddress
    }

def get_flag(spawner):
    r = pwn.remote(*spawner)
    r.recvuntil(b"action? ")
    r.sendline(b"3")

    return r.recvall(timeout=2.).decode()
