#%%
import re
import bisect
import mmap
from dataclasses import dataclass
from collections import defaultdict
import sqlite3
from database.frequency_count import RequestCounts 
from database.endpoint import EndpointCount
from database.suspicious import SuspecioisActivity
from transform.transform import Transform
from concurrent.futures import ThreadPoolExecutor
import pprint
# conn = sqlite3.connect('logs.db')
# cur = conn.cursor()
# # create table if it doesnot exist
# # IP request counts, most accessed endpoint, and suspicious activity detection.
# cur.execute('''CREATE TABLE IF NOT EXISTS request_counts()''')
get_ip = lambda string:re.search(r'^\d{0,3}.\d{0,3}.\d{0,3}.\d{0,3}\b', string)

get_endpoint = lambda string: re.search(r'\s"\S+\s+(?P<endpoint>\S+)\s+\S+"\s', string)

invalid_cred = lambda string:re.search(r'"Invalid credentials"$', string)

http_status = lambda string:re.search(r'\s\d+\s', string)

ERROR_CODES = [400, 401, 403, 404, 405, 500, 501, 502, 503, 504, 505]
NO_THREADS = 12

# @dataclass
# class Log:
#     IP: str
#     Endpoint: str
#     Invalid_Credentials: bool
#     HTTP_Status: int

ip_count = {}

# @dataclass
# class EndpointData:
#     endpoint: str
#     count: int

request_counts = RequestCounts()
most_frequent_endpoint = EndpointCount()
suspeciois_activity = SuspecioisActivity()

import queue
from queue import Queue
import time
# reading each line from file on a thread and updating it to a Queue

request_count = Queue()
endpoint_count = Queue()
suspicious_activity = Queue()


#%%
def regex_extractor(chunk: list, request_count: Queue, endpoint_count: Queue, suspicious_activity: Queue):
    for line in chunk:
        if ip:=get_ip(line):
            ip = ip.group(0)
        if ip:
            request_count.put(ip)
        else:
            continue

        endpoint = get_endpoint(line)
        if endpoint:
            endpoint_count.put(endpoint)
        endpoint_count.put(endpoint)

        credits = invalid_cred(line)
        http_status_code = http_status(line)

        if credits and http_status_code and ip:
            status_code = int(http_status_code.group(0))
            if status_code in ERROR_CODES:
                suspicious_activity.put(ip)
                suspicious_activity.put(ip)

    # None flag to indicate the end of the chunk of data         
    request_count.put("END")
    endpoint_count.put(None)
    suspicious_activity.put(None)

def main():
    start_time = time.time()

    # load the data file and split it into chunks
    with open('sample.log', 'r') as file:
        lines = file.readlines()
        chunk_size = len(lines) // NO_THREADS
        chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]
        if len(lines) % NO_THREADS != 0:
            if chunks[-1]:
                chunks[-2].extend(chunks[-1])
                chunks = chunks[:-1]
        transform_data = Transform(request_count, endpoint_count, suspicious_activity, len(chunks))
        # Assign each chunk to a thread
        with ThreadPoolExecutor(max_workers=NO_THREADS+1) as executor:
            for chunk in chunks:
                executor.submit(regex_extractor, chunk, request_count, endpoint_count, suspicious_activity)
            # while all the other threads are running execute the transform thread which is a class inherited 
            # from threading.Thread
            # pass all the Queues to the class to update the data
            # executor.submit(transform_data.run)
            transform_data.run()
        #transform_data.run()

    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    pprint.pprint(transform_data.ip_count)

if __name__ == "__main__":
    main()
#%%

# def main():
#     with open('sample.log', 'r') as file:

#         lines = file.readlines()
        
#         for i in range(len(lines)):
#             line = lines[i]
#             # print(line.strip())

#             if ip:=get_ip(line):
#                 ip = ip.group(0)
                
#             if ip:
#                 request_counts.insert_update_data({'IP': ip})

#             if endpoint:=get_endpoint(line):
#                 endpoint = endpoint.group('endpoint')
#                 if endpoint:
#                     most_frequent_endpoint.insert_update_data({'Endpoint': endpoint})
#                 most_frequent_endpoint.insert_update_data({'Endpoint': endpoint})    
            
#             credits = invalid_cred(line)
#             http_status_code = http_status(line)

#             if credits and http_status_code:
#                 status_code = int(http_status_code.group(0))
#                 if status_code in ERROR_CODES:
#                     if ip:
#                         suspeciois_activity.insert_update_data({'IP': ip})
                

            # suspeciois_activity.insert_update_data({'IP':ip})
        # print(credits, http_status_code)
        # if invalid_cred(line) and http_status(line) in ERROR_CODES:
        #     print("Invalid credentials")
        #     suspeciois_activity.insert_update_data({'IP':ip})

        # if endpoint:=get_endpoint(line):
        #     endpoint = endpoint.group('endpoint')
        #     print(f"Endpoint: {endpoint}")
        
        # if invalid_cred(line):
        #     print("Invalid credentials")
        
        # if status:=http_status(line):
        #     status = status.group(0)
        #     print(f"HTTP Status: {status}")
        
        

# request_counts.export_data('output.csv')
# %%
