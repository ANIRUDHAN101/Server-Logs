from queue import Queue
from regex import get_ip, get_endpoint, invalid_cred, http_status
from typing import Any


def regex_extractor(chunk: Any, end_index: int, 
                    request_count: Queue, 
                    endpoint_count: Queue, 
                    suspicious_activity: Queue,
                    error_codes: list[int]) -> None:
    """
        This function run as the producer thread,
        it extracts the IP address, endpoint, and HTTP status code from the log file
        and puts the data in the respective queues
        args:
            chunk: Any: the chunk of data to process
            end_index: int: the end index of the chunk
            request_count: Queue: the queue to store the IP address
            endpoint_count: Queue: the queue to store the endpoint
            suspicious_activity: Queue: the queue to store the suspicious activity
    """

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
            
            if status_code in error_codes:

                suspicious_activity.put(ip)

    # "END" flag to indicate the end of the chunk of data         
    request_count.put("END")