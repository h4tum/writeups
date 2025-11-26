import re


def restore_password(content: str):
    lines_with_question_mark = [line for line in content.split("\n") if "?" in line]

    hex_parts = [re.sub(r"[^a-f0-9]", "", line) for line in lines_with_question_mark]

    hex_string = "".join(hex_parts)

    hex_string = hex_string.replace("dd", "")

    transformed_string = "flag{" + hex_string[5:]

    final_flag = transformed_string[:-1] + "}"

    return final_flag


with open(".pwfault", "r") as f:
    recovered_password = restore_password(f.read())
    print(recovered_password)
