import csv
from database.db import Database
THRESHOLD = 10

class SuspecioisActivity(Database):
    def __init__(self):
        super().__init__(db_name='logs.db', table_name='suspicious_activity')

    def create_table(self): 
        """Creates a table suspicious_activity with columns (IP, counts) """
        
        self.cur.execute('''
                            CREATE TABLE IF NOT EXISTS 
                            suspicious_activity(IP TEXT PRIMARY KEY, counts INTEGER)
                         ''')
        
        self.conn.commit()
    
    def insert_update_data(self, data):
        """ This method inserts or updates the data in the table suspicious_activity
            If the IP address is already present in the table, the count will be updated.
            If the IP address is not present in the table, a new row will be inserted.
        """

        ip = data.get('IP')
        self.cur.execute('''
                            INSERT INTO suspicious_activity(IP, counts)
                            VALUES(?, 1)
                            ON CONFLICT(IP) DO UPDATE SET 
                            counts = counts + 1
                            ''', (ip,))
        self.conn.commit()

    def export_data(self, file_name):
        """ This method fetches the data from table suspicious_activity
            in descending order and exports it to a csv file.
            A new csv file will be created if a file already does not exist.
        """

        self.cur.execute('''
                    SELECT * FROM suspicious_activity
                    WHERE counts > ?
                    ORDER BY counts DESC
                    ''', (THRESHOLD,))
        
        data = self.cur.fetchall()

        with open(file_name, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['IP Address', 'Failed Login Count'])
            csv_writer.writerows(data)