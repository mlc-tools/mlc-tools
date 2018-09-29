import sqlite3
import MySQLdb
import psycopg2


class DataBase:

    def __init__(self):
        pass

    def __del__(self):
        self._close()

    def _connect(self):
        pass

    def _close(self):
        pass

    def query(self, query):
        pass

    def query_raw(self, query):
        pass

    def iterate(self, response):
        pass


class DataBaseCursor(DataBase):

    def __init__(self, dbtype):
        self.dbtype = dbtype
        self.conn = None
        self.cursor = None
        DataBase.__init__(self)

    def connect(self, host, database, user, psw):

        if self.dbtype == 'sqlite':
            self._connect_sqlite(host, database, user, psw)
        elif self.dbtype == 'mysql':
            self._connect_mysql(host, database, user, psw)
        elif self.dbtype == 'postgresql':
            self._connect_postresql(host, database, user, psw)

        self.cursor = self.conn.cursor()

    def _connect_sqlite(self, host, database, user, psw):
        self.conn = sqlite3.connect(database + '.db')

    def _connect_mysql(self, host, database, user, psw):
        self.conn = MySQLdb.connect(host, user, psw, database)

    def _connect_postresql(self, host, database, user, psw):
        self.conn = psycopg2.connect(host=host, dbname=database, user=user, password=psw)

    def _close(self):
        if self.conn:
            self.conn.close()

    def query_one(self, query):
        try:
            self.cursor.execute(query)
            row = self.cursor.fetchone()
            row = [str(cell) for cell in (row if row else [])]
            return row
        except psycopg2.ProgrammingError:
            return []

    def query_all(self, query):
        try:
            self.cursor.execute(query)
            table = self.cursor.fetchall()
            if isinstance(table, tuple):
                table = list(table)
            if not table:
                return []
            for i, row in enumerate(table):
                table[i] = [str(cell) for cell in row]
            return table
        except psycopg2.ProgrammingError:
            return []


class DataBaseMysql(DataBaseCursor):

    def __init__(self):
        DataBaseCursor.__init__(self, 'mysql')


class DataBaseSqlite(DataBaseCursor):

    def __init__(self):
        DataBaseCursor.__init__(self, 'sqlite')


class DataBasePostgreSql(DataBaseCursor):

    def __init__(self):
        DataBaseCursor.__init__(self, 'postgresql')
