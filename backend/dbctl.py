import oracledb.connection as conn
from os import getenv
from dotenv import load_dotenv, find_dotenv


class DBContextManager:
    def __init__(self):
        load_dotenv(find_dotenv())
        self._connection = None

    def __enter__(self):
        try:
            self._connection = conn.connect(
                user=getenv('ORACLE_DB_USER'),
                password=getenv('ORACLE_DB_PASSWORD'),
                host=getenv('ORACLE_DB_HOST'),
                port=getenv('ORACLE_DB_PORT'),
                service_name=getenv('ORACLE_DB_SERVICE_NAME'),  
                encoding='UTF-8',
                disable_oob=True
            )
            return self._connection.cursor()
        except Exception:
            pass

    def __exit__(self, exc_type, exc_value, exc_traceback):
        try:
            self._connection.cursor().close()
            self._connection.close()
            self._connection = None
        except Exception:
            pass
