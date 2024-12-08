import csv
import os

def save_log_csv(file: str, data: list, header: list, heading: str, mode: str = 'w') -> None:
    """
        This function saves the data to a csv file
    """

    with open(file, mode, newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([heading])
        writer.writerow(header)
        writer.writerows(data)

def save(file: str, data_log_count, data_max_endpoint, data_suspicious_ip_index) -> None:
    """
        This function saves the data to a csv file
    """
    if os.path.exists(file):
        os.remove(file)
    
    save_log_csv(file, data_log_count, ['IP Address', 'Request Count'], heading='Requests per IP')
    save_log_csv(file, data_max_endpoint, ['Endpoint', 'Access Count'], heading='Most Accessed Endpoint', mode='a')
    save_log_csv(file, data_suspicious_ip_index, ['IP Address', 'Failed Login Count'], heading='Suspicious Activity', mode='a')