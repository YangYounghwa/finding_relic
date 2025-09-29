import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()
import logging
logger = logging.getLogger(__name__)
from contextlib import contextmanager


class Database:
    def __init__(self):
        self.db_url = os.getenv("SUPABASE_URL")
        if not self.db_url:
            raise ValueError("SUPABASE_URL environment variable not set")
        
    @contextmanager
    def get_connection(self):
        """Provides a database connections."""
        conn = None
        try:
            conn=psycopg2.connect(self.db_url)
            yield conn
        except psycopg2.Error as e:
            logger.error(f"Error connecting to the database: {e}")
            raise
        finally:
            if conn is not None:
                conn.close()
                
db_manager = Database()