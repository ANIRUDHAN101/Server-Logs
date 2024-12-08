from database.db import Database
import csv
class RequestCounts(Database):
    def __init__(self):
        super().__init__(db_name='logs.db', table_name='request_counts')

    def create_table(self): 
        """Creates a table request_counts with columns (IP, counts) """
        
        self.cur.execute('''
                            CREATE TABLE IF NOT EXISTS 
                            request_counts(IP TEXT PRIMARY KEY, counts INTEGER)
                         ''')
        
        self.conn.commit()
    
    def insert_update_data(self, data):
        """ This method inserts or updates the data in the table request_counts
            If the IP address is already present in the table, the count will be updated.
            If the IP address is not present in the table, a new row will be inserted.
        """

        ip = data.get('IP')
        self.cur.execute('''
                            INSERT INTO request_counts(IP, counts)
                            VALUES(?, 1)
                            ON CONFLICT(IP) DO UPDATE SET 
                            counts = counts + 1
                            ''', (ip,))
        self.conn.commit()

    def export_data(self, file_name):
        """ This methos fetches the data from table request_counts
            in descnding orderand exports it to a csv file.
            A new csv file will be created if a file already doesnot exit.
        """

        self.cur.execute('''
                            SELECT * FROM request_counts
                            ORDER BY counts DESC
                            ''')
        data = self.cur.fetchall()

        with open(file_name, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['IP Address', 'Request Count'])
            csv_writer.writerows(data)
    