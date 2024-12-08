import csv
import os

def save_log_csv(file: str, data: list, header: list, heading: str, mode: str = 'w') -> None:
    """
        This function saves the data to a csv file
        args:
            file: str: the file to save the data to
            data: list: the data to save
            header: list: the header of the data
            heading: str: the heading of the data
            mode: str: the mode to open the file
    """

    with open(file, mode, newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([heading])
        writer.writerow(header)
        writer.writerows(data)

def save(file: str, data_log_count, data_max_endpoint, data_suspicious_ip_index) -> None:
    """
        This function saves the data to a csv file
        args:
            file: str: the file to save the data to
            data_log_count: list: the data to save
            data_max_endpoint: list: the header of the data
            data_suspicious_ip_index: str: the heading of the data
    """
    if os.path.exists(file):
        os.remove(file)
    
    save_log_csv(file, data_log_count, ['IP Address', 'Request Count'], heading='Requests per IP')
    save_log_csv(file, data_max_endpoint, ['Endpoint', 'Access Count'], heading='Most Accessed Endpoint', mode='a')
    save_log_csv(file, data_suspicious_ip_index, ['IP Address', 'Failed Login Count'], heading='Suspicious Activity', mode='a')