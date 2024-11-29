import psycopg2
from psycopg2.extras import execute_values
import datetime

class TimescaleDBClient:
    def __init__(self, host="localhost", port=5432, database="monitoring", user="admin", password="password"):
        self.conn = None
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        """Establish a connection to the TimescaleDB."""
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.database,
                user=self.user,
                password=self.password
            )
            print("Connected to TimescaleDB")
        except Exception as e:
            print(f"Error connecting to TimescaleDB: {e}")
            raise

    def create_table(self):
        # TODO timestamp without a TZ
        # TODO Add all metrics columns
        """Create a table for storing metrics if it doesn't already exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS system_metrics (
            id SERIAL,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            cpu_usage_percent DOUBLE PRECISION NOT NULL,
            memory_usage_percent DOUBLE PRECISION NOT NULL,
            disk_usage_percent DOUBLE PRECISION NOT NULL
        );
        SELECT create_hypertable('system_metrics', 'timestamp', if_not_exists => TRUE);
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(create_table_query)
                self.conn.commit()
                print("Table created or already exists.")
        except Exception as e:
            print(f"Error creating table: {e}")
            self.conn.rollback()
            raise

    def insert_metric(self, timestamp, cpu_usage, memory_usage, disk_usage):
        """Insert a single metric row into the table."""
        insert_query = """
        INSERT INTO system_metrics (timestamp, cpu_usage_percent, memory_usage_percent, disk_usage_percent)
        VALUES (%s, %s, %s, %s);
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(insert_query, (timestamp, cpu_usage, memory_usage, disk_usage))
                self.conn.commit()
                print("Metric inserted successfully.")
        except Exception as e:
            print(f"Error inserting metric: {e}")
            self.conn.rollback()
            raise

    def bulk_insert_metrics(self, metrics):
        """
        Insert multiple metrics rows at once.
        :param metrics: List of tuples (timestamp, cpu_usage, memory_usage, disk_usage)
        """
        insert_query = """
        INSERT INTO system_metrics (timestamp, cpu_usage_percent, memory_usage_percent, disk_usage_percent)
        VALUES %s;
        """
        try:
            with self.conn.cursor() as cursor:
                execute_values(cursor, insert_query, metrics)
                self.conn.commit()
                print(f"{len(metrics)} metrics inserted successfully.")
        except Exception as e:
            print(f"Error bulk inserting metrics: {e}")
            self.conn.rollback()
            raise

    def close(self):
        """Close the connection to the TimescaleDB."""
        if self.conn:
            self.conn.close()
            print("Connection closed.")
