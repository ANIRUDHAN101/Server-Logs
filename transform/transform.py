import queue
from queue import Queue
import threading

class Transform(threading.Thread):
    """
        This class saves and the extracted data from the logs
        It ensures the data are saved in a descending sorted order
    """

    def __init__(self, request_count: Queue, endpoint_count: Queue, suspicious_activity: Queue, producers: int) -> None:
        super().__init__()
        self.ip_count_index = {}
        self.suspicious_ip_index = {}
        self.max_endpoint = {}

        self.ip_count = []
        self.suspicious_count = []

        self.request_count = request_count
        self.endpoint_count = endpoint_count
        self.suspicious_activity = suspicious_activity
        self.producers = producers

    def __request_count_update(self, ip: str) -> None:
        """
            This method updates the request count for the given IP address
        """
        if ip in self.ip_count_index:
            index = self.ip_count_index[ip]
            # update the count of the IP address in the list self.ip_count
            self.ip_count[index] = (ip, self.ip_count[index][1] + 1)

            # sort the list in descending order
            # if the updated ip is larger than the ip to the left of it, swap the elements
            # till the ip is in the correct position
            while index > 0 and self.ip_count[index-1][1] < self.ip_count[index][1]:
                # swap the elements
                self.ip_count[index], self.ip_count[index-1] = self.ip_count[index-1], self.ip_count[index]
                self.ip_count_index[self.ip_count[index][0]] = index
                index -= 1

        else:
            # if the IP address is not present in the list, add it to the list
            index = len(self.ip_count)
            self.ip_count.append((ip, 1))
            
        self.ip_count_index[ip] = index
    

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
                self.__request_count_update(ip)
        

        # while not self.endpoint_count.empty():
        #     data = self.endpoint_count.get()
        #     endpoint = data.get('Endpoint')
        #     count = data.get('Count')
        #     self.max_endpoint[endpoint] = count

        # while not self.suspicious_activity.empty():
        #     data = self.suspicious_activity.get()
        #     ip = data.get('IP')
        #     count = data.get('Count')
        #     self.suspicious_ip_index[ip] = count

    def run(self):
        self.transform_data()