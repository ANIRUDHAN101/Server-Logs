import re

get_ip = lambda string:re.search(r'^\d{0,3}.\d{0,3}.\d{0,3}.\d{0,3}\b', string)

get_endpoint = lambda string: re.search(r'\s"\S+\s+(?P<endpoint>\S+)\s+\S+"\s', string)

invalid_cred = lambda string:re.search(r'"Invalid credentials"$', string)

http_status = lambda string:re.search(r'\s\d+\s', string)