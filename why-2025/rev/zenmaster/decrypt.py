import json
import multiprocessing
import os
import time

obfuscated_data = [
    0x3A1BD1D0,
    0x6A4F82D3,
    0x6A188583,
    0x6F148381,
    0x6F4E83D3,
    0x694D86D0,
    0x3D1F8CD2,
    0x6D1BD0D1,
]


def decode_flag(key: int) -> str:
    flag = "flag{"

    for data in obfuscated_data:
        decrypted_dword = data ^ key
        flag += decrypted_dword.to_bytes(4, byteorder="little").decode("ascii")

    flag += "}"

    return flag


def is_valid_char_code(code: int) -> bool:
    is_digit = (code >= ord("0")) and (code <= ord("9"))
    is_lower = (code >= ord("a")) and (code <= ord("f"))
    return is_digit or is_lower


def solve_for_key():
    print("Starting key search... This may take a minute.")

    flags: dict[int, str] = dict()

    for key in range(2**32):
        all_chunks_are_valid = True

        for data in obfuscated_data:
            decrypted_dword = data ^ key

            b1 = decrypted_dword & 0xFF
            b2 = (decrypted_dword >> 8) & 0xFF
            b3 = (decrypted_dword >> 16) & 0xFF
            b4 = (decrypted_dword >> 24) & 0xFF

            if not (is_valid_char_code(b1) and is_valid_char_code(b2) and is_valid_char_code(b3) and is_valid_char_code(b4)):
                all_chunks_are_valid = False
                break

        if all_chunks_are_valid:
            flag = decode_flag(key)
            print(f"Decryption Key (Hex): {hex(key)}, Flag: {flag}")
            flags[key] = flag

    print(f"Summary:\n{flags}")


def search_key_range(r: range) -> dict[int, str]:
    local_flags: dict[int, str] = {}

    for key in r:
        all_chunks_are_valid = True
        for data in obfuscated_data:
            decrypted_dword = data ^ key

            b1 = decrypted_dword & 0xFF
            b2 = (decrypted_dword >> 8) & 0xFF
            b3 = (decrypted_dword >> 16) & 0xFF
            b4 = (decrypted_dword >> 24) & 0xFF

            if not (is_valid_char_code(b1) and is_valid_char_code(b2) and is_valid_char_code(b3) and is_valid_char_code(b4)):
                all_chunks_are_valid = False
                break

        if all_chunks_are_valid:
            flag = decode_flag(key)
            print(f"Worker (PID: {os.getpid()}) found candidate Key: {hex(key)}, Flag: {flag}")
            local_flags[key] = flag

    return local_flags


def solve_for_key_multithreaded():
    num_processes = os.cpu_count() or 4
    print(f"Starting key search using {num_processes} parallel processes...")

    total_keys = 2**32
    chunk_size = total_keys // num_processes
    ranges: list[range] = []
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size
        # Ensure the last chunk covers the entire remaining range
        if i == num_processes - 1:
            end = total_keys
        ranges.append(range(start, end))

    start_time = time.time()

    with multiprocessing.Pool(processes=num_processes) as pool:
        results = pool.map(search_key_range, ranges)

    all_flags: dict[int, str] = {}
    for result_dict in results:
        all_flags.update(result_dict)

    end_time = time.time()

    print(f"\nSearch completed in {end_time - start_time:.2f} seconds.")
    print(f"Summary of all found keys and flags:\n{json.dumps(all_flags, indent=2)}")


if __name__ == "__main__":
    solve_for_key_multithreaded()
