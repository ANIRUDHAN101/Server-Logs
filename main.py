import argparse
import re
from queue import Queue
import time
from consumer import Consumer
from concurrent.futures import ThreadPoolExecutor
from producer import regex_extractor
from lazy_files import get_chunk_files
import pprint
import mmap
from save_log_csv import save
from print_template import (
    display_suspicious_activity, 
    display_most_accessed_endpoint, 
    display_ip_request_counts
)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Log Processing Tool")
    parser.add_argument("--threads", type=int, default=12, help="Number of threads to use")
    parser.add_argument(
        "--threshold", 
        type=int, 
        default=5, 
        help="Threshold for detecting suspicious activity"
    )
    parser.add_argument(
        "--errorcodes", 
        type=int, 
        nargs="+", 
        default=[400, 401, 403, 404, 405, 500, 501, 502, 503, 504, 505],
        help="List of HTTP error codes to consider as suspicious"
    )
    parser.add_argument("--input", type=str, default="./data/sample.log", help="Path to the input log file")
    parser.add_argument("--output", type=str, default="./data/output.csv", help="Path to the output CSV file")
    args = parser.parse_args()

    # Assign arguments to variables
    NO_THREADS = args.threads
    sususpicious_THRESHOLD = args.threshold
    ERROR_CODES = args.errorcodes
    input_file = args.input
    output_file = args.output

    # Initialize queues
    request_count = Queue()
    endpoint_count = Queue()
    suspicious_activity = Queue()

    start_time = time.time()

    # Load the data file and split it into chunks
    with open(input_file, 'r+b') as file:
        file = mmap.mmap(file.fileno(), 0)
        chunks_indexs = get_chunk_files(file, NO_THREADS)

        consumer = Consumer(
            request_count,
            endpoint_count,
            suspicious_activity,
            NO_THREADS,
            sususpicious_activity_thresholds=sususpicious_THRESHOLD
        )

        # Assign each chunk to a thread
        with ThreadPoolExecutor(max_workers=NO_THREADS + 1) as executor:
            for chunk_index in chunks_indexs:
                executor.submit(regex_extractor, file, chunk_index, request_count, endpoint_count, suspicious_activity)

            # Run the consumer
            consumer.run()

    end_time = time.time()
    

    # Save results to CSV
    save(output_file, 
         consumer.ip_count, 
         consumer.max_endpoint, 
         consumer.suspicious_count)

    # Display results
    display_ip_request_counts(consumer.ip_count)
    print('\n')
    display_most_accessed_endpoint(consumer.max_endpoint[0])
    print('\n')
    display_suspicious_activity(consumer.suspicious_count)
    print(f"Execution time: {end_time - start_time} seconds")
    
if __name__ == "__main__":
    main()
