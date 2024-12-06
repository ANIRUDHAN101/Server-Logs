import re
import bisect
import mmap

get_ip = lambda string:re.search(r'^\d{0,3}.\d{0,3}.\d{0,3}.\d{0,3}\b', string)

get_endpoint = lambda string: re.search(r'\s"\S+\s+(\S+)\s+\S+"\s', string)[1]

invalid_cred = lambda string:re.search(r'"Invalid credentials"$', string)

http_status = lambda string:re.search(r'\s\d+\s', string)

with open('sample.log', 'r+b') as file:
    mm = mmap.mmap(file.fileno(), 0)

    lines = mm.readlines()
    line = lines[0]
    print(line.strip())