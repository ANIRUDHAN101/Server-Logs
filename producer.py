from queue import Queue
from regex import get_ip, get_endpoint, invalid_cred, http_status
from typing import Any
ERROR_CODES = [400, 401, 403, 404, 405, 500, 501, 502, 503, 504, 505]

def regex_extractor(chunk: Any, end_index: int, 
                    request_count: Queue, 
                    endpoint_count: Queue, 
                    suspicious_activity: Queue):

    while chunk.tell() < end_index:
        line = chunk.readline().decode('utf-8')
        if ip:=get_ip(line):
            ip = ip.group(0)
        if ip:
            request_count.put(ip)
        else:
            continue

        endpoint = get_endpoint(line).group('endpoint')
        if endpoint:
            endpoint_count.put(endpoint)

        credits = invalid_cred(line)
        http_status_code = http_status(line)

        if credits and http_status_code and ip:
            status_code = int(http_status_code.group(0))
            
            if status_code in ERROR_CODES:

                suspicious_activity.put(ip)

    # None flag to indicate the end of the chunk of data         
    request_count.put("END")