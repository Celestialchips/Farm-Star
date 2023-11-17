import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = self.connect_to_database(host, user, password, database)
    
    @staticmethod
    def connect_to_database(host, user, password, database):
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return connection

    @staticmethod
    def fetch_data_from_table(connection, table_name):
        cursor = connection.cursor(dictionary=True)
        query = f"SELECT longitude, latitude FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results

    def fetch_data(self, table_name):
        return self.fetch_data_from_table(self.connection, table_name)

    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()
