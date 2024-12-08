import csv
from database.db import Database

class EndpointCount(Database):
    def __init__(self):
        super().__init__(db_name='logs.db', table_name='endpoint_counts')

    def create_table(self): 
        """Creates a table endpoint_counts with columns (Endpoint, counts) """
        
        self.cur.execute('''
                            CREATE TABLE IF NOT EXISTS 
                            endpoint_counts(Endpoint TEXT PRIMARY KEY, counts INTEGER)
                         ''')
        
        self.conn.commit()
    
    def insert_update_data(self, data):
        """ This method inserts or updates the data in the table endpoint_counts
            If the endpoint is already present in the table, the count will be updated.
            If the endpoint is not present in the table, a new row will be inserted.
        """

        endpoint = data.get('Endpoint')
        self.cur.execute('''
                            INSERT INTO endpoint_counts(Endpoint, counts)
                            VALUES(?, 1)
                            ON CONFLICT(Endpoint) DO UPDATE SET 
                            counts = counts + 1
                            ''', (endpoint,))
        self.conn.commit()

    def export_data(self, file_name):
        """ This method fetches the most accessed endpoint from the table endpoint_counts
            and updates it to the csv file.
            (Note this fucntion appends the data to the file if it already exists)
        """
        self.cur.execute('''
                            SELECT * FROM endpoint_counts
                            ORDER BY counts DESC
                            LIMIT 1
                            ''')
        data = self.cur.fetchone()
        
        with open(file_name, 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['Endpoint', 'Access Count'])
            csv_writer.writerow(data)

