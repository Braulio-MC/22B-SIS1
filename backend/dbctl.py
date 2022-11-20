import oracledb.connection as conn
from os import getenv


class DBCTL:
    def __init__(self):
        self._connection = None
        self._cursor = None

    def open_connection(self):
        try:
            self._connection = conn.connect(
                user=getenv('ORACLE_DB_USER'),  # type: ignore
                password=getenv('ORACLE_DB_PASSWORD'),  # type: ignore
                host=getenv('ORACLE_DB_HOST'),  # type: ignore
                port=getenv('ORACLE_DB_PORT'),  # type: ignore
                service_name=getenv('ORACLE_DB_SERVICE_NAME'),  # type: ignore  
                encoding='UTF-8',
                disable_oob=True
            )
        except Exception as ex:
            print(ex)

    def get_cursor(self):
        if self._connection:
            return self._connection.cursor()
        return None

    def close_connection(self):
        if self._connection:
            self._connection.cursor().close()
            self._connection.close()
            self._connection = None
        else:
            pass
