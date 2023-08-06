import pymysql
from injector import inject, Injector

from .wrapperabstraction import MySQLWrapperAbstract
from .mysqlquerries import MySQLQueryStatements
from .connections import MysqlConnection, get_configurations


class MySQLWrapper(MySQLWrapperAbstract):
    """ Wrapper class """

    @inject
    def __init__(self, connection: pymysql.connect, sql: MySQLQueryStatements):
        self.connection = connection
        self.table_object = sql

    @staticmethod
    def start():
        """ Static method creating an instance of the connection """
        
        injector = Injector([get_configurations, MysqlConnection])
        wrapper = injector.get(MySQLWrapper)
        return wrapper

    def create_table(self, table_name, columns):
        """ Create table function """

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.table_object.sanitize_create_table(table_name, columns))
        self.connection.commit()

    def insert_values(self, table, columns, values):
        """ Insert values """

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.table_object.sanitize_insert_full(table, columns, values))
        self.connection.commit()

    def fetch_all(self, table):
        """ Fetch all records """

        all_records = {}
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.table_object.sanitize_fetch_all(table))
            all_records = cursor.fetchall()
        self.connection.commit()
        return all_records

    def fetch_limit(self, table, value):
        """ fetch specific records """

        lim = {}
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.table_object.sanitize_fetch_limit(table, value))
            lim = cursor.fetchone()
        self.connection.commit()
        return lim

    def update_table(self, table, column, new_value, conditional_column, conditional_value):
        """ Update table """

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.table_object.santize_update(table, column, new_value, conditional_column, conditional_value))
        self.connection.commit()

    def delete_table(self, table):
        """ Delete table """

        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute(self.table_object.sanitize_delete_table(table))
        self.connection.commit()
