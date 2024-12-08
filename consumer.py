import queue
from queue import Queue
import threading

class Consumer(threading.Thread):
    """
        This class saves and the extracted data from the logs
        It ensures the data are saved in a descending sorted order
    """

    def __init__(self, 
                 request_count: Queue, 
                 endpoint_count: Queue, 
                 suspicious_activity: Queue, 
                 producers: int, 
                 sususpicious_activity_thresholds=10) -> None:
        
        super().__init__()
        self.ip_count_index = {}
        self.suspicious_ip_index = {}
        self.endpoint_count_dict = {}
        self.max_endpoint = []

        self.ip_count = []
        self.suspicious_count = []

        self.request_count = request_count
        self.endpoint_count = endpoint_count
        self.suspicious_activity = suspicious_activity
        self.producers = producers
        self.suspicious_activity_threshold = sususpicious_activity_thresholds

    def __request_count_update(self, ip: str, count_index :dict, count: list) -> None:
        """
            This method updates the request count for the given IP address
        """
        if ip in count_index:
            index = count_index[ip]
            # update the count of the IP address in the list self.count
            count[index] = (ip, count[index][1] + 1)

            # sort the list in descending order
            # if the updated ip is larger than the ip to the left of it, swap the elements
            # till the ip is in the correct position
            while index > 0 and count[index-1][1] < count[index][1]:
                # swap the elements
                count[index], count[index-1] = count[index-1], count[index]
                count_index[count[index][0]] = index
                index -= 1

        else:
            # if the IP address is not present in the list, add it to the list
            index = len(count)
            count.append((ip, 1))
            
        count_index[ip] = index


    def __request_max_update(self, new_data: str, count_dict: dict, max_count: list) -> None:

        """
            This method updates the maximum request count for the given endpoint
        """
        # print(new_data, count_dict, max_count)
        if new_data in count_dict:
            count_dict[new_data] += 1
            if max_count and count_dict[new_data] > max_count[0][1]:
                max_count[0] = (new_data, count_dict[new_data])
        else:
            count_dict[new_data] = 1
            if not max_count:
                max_count.append((new_data, 1))

    def transform_data(self):
        """
            This method transforms the data from the queues and stores it in the class attributes
        """
        ended_producers_count = 0

        while True:
            if ended_producers_count == self.producers:
                break
            if not self.request_count.empty():
                ip = self.request_count.get()
                if ip == "END":
                    ended_producers_count += 1
                    continue
                self.__request_count_update(ip, self.ip_count_index, self.ip_count)
        

            if not self.endpoint_count.empty():
                endpoint = self.endpoint_count.get()
                # print(endpoint)
                self.__request_max_update(endpoint, self.endpoint_count_dict, self.max_endpoint)

            if not self.suspicious_activity.empty():
                ip = self.suspicious_activity.get()
                self.__request_count_update(ip, self.suspicious_ip_index, self.suspicious_count)

        # threshold the suspecious activity to SUSPICIOUS_ACTIVITY_THRESHOLD
        self.suspicious_count = [data for data in self.suspicious_count if data[1] > self.suspicious_activity_threshold]


    def run(self):
        self.transform_data()