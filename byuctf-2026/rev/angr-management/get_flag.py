from pwn import *


def main():
    # r = process("./angr_management_test")
    r = remote("chals.cyberjousting.com", 1368)

    sequence = [
        256,
        423,
        495,
        307,
        39,
        250,
        391,
        119,
        105,
        499,
        123,
        104,
        536,
        257,
        608,
        253,
        74,
        365,
        543,
        300,
        571,
        506,
        595,
        192,
        383,
        112,
        17,
        556,
        93,
        318,
        114,
        276,
        18,
        216,
        449,
        414,
        124,
        503,
        71,
        407,
        78,
        285,
        481,
        66,
        381,
        531,
        82,
        337,
        600,
        86,
        230,
        327,
        472,
        393,
        348,
        331,
        14,
        207,
        402,
        548,
        528,
        168,
        530,
        490,
        378,
        408,
        518,
        202,
        87,
        342,
        329,
        624,
    ]

    for num in sequence:
        r.sendline(str(num).encode())

    print(r.recvall().decode())


if __name__ == "__main__":
    main()
