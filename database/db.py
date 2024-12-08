import sqlite3
from abc import ABC, abstractmethod
import csv
    
class Database(ABC):
    """This class handles the storing of the extracted data in a sqlite3 database

    Args:
        db_name (str): The name of the database to connect to
        table_name (str): The name of the table to create in the database 
                          (Note if the table doesnot exit it will be created)

    Attributes:
        conn (sqlite3.Connection): The connection object to the database
        cur (sqlite3.Cursor): The cursor object to the database
        table_name (str): The name of the table 

    Methods:
        create_table(): Creates a table in the database if it doesnot exist
        insert_update_data(data: dict): Inserts or update data into the table
        export_data(file_name: str): Export the data from the table to csv file
    """

    def __init__(self, db_name: str, table_name: str, **kwargs):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.table_name = table_name
        self.create_table(**kwargs)
    
    def __del__(self):
        self.conn.close()
    
    @abstractmethod
    def create_table(self):
        """Creates a table in the database if it doesnot exist"""
        pass
    
    @abstractmethod
    def export_data(self, file_name: str):
        """Export the data from the table to csv file

        Args:
            file_name (str): The name of the file to export the data to
        """
        pass
    
    @abstractmethod
    def insert_update_data(self, data: dict):
        """Inserts or update data into the table

        Args:
            data (dict): The data to insert or update in the table
        """
        pass

    
