import os
import sys

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

IV = b"R4ND0MivR4ND0Miv"
PW = "L0s3@llYourF1l3s"


def derive_key(password: str) -> bytes:
    key = password.encode("utf-8")

    return (key + b"\0" * 16)[:16]


def decrypt_file(encrypted_file_path: str, password: str):
    decrypted_file_path = os.path.splitext(encrypted_file_path)[0]

    # Check for a '.enc' extension to ensure we are decrypting the correct file
    if not encrypted_file_path.endswith(".enc"):
        print("Error: The file to decrypt must have a '.enc' extension.", file=sys.stderr)
        return

    if os.path.exists(decrypted_file_path):
        print(f"Error: Output file '{decrypted_file_path}' already exists. Please move or delete it before decrypting.", file=sys.stderr)
        return

    try:
        with open(encrypted_file_path, "rb") as f_in:
            encrypted_data = f_in.read()

        key = derive_key(password)
        cipher = AES.new(key, AES.MODE_CBC, IV)

        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        with open(decrypted_file_path, "wb") as f_out:
            f_out.write(decrypted_data)

        print(f"Success: Decrypted '{encrypted_file_path}' to '{decrypted_file_path}'")

    except FileNotFoundError:
        print(f"Error: The file '{encrypted_file_path}' was not found.", file=sys.stderr)
    except (ValueError, KeyError):
        print("Error: Decryption failed. This is likely due to an incorrect password.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <file_to_decrypt.enc>", file=sys.stderr)
        sys.exit(1)

    file_arg = sys.argv[1]

    decrypt_file(file_arg, PW)
