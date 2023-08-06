import pymysql
import os
from injector import Key, Module, provider, singleton
from collections import namedtuple

database_configurations = Key('db_config')

def get_configurations(binder):
    """ Add connection attributes """

    Configuration = namedtuple('Configuration', 'host user password database')
    configt = Configuration(host = os.getenv('host'), user = os.getenv('user'), password = os.getenv('password'), database=os.getenv('database'))
    binder.bind(database_configurations, to=configt, scope=singleton)

class MysqlConnection(Module):
    """ connection class """

    @provider
    @singleton
    def connect(self, configuration: database_configurations) -> pymysql.connect:
        """ Connect to the db """ 
        connection = pymysql.connect(host=configuration.host,
                                     password = configuration.password,
                                     user = configuration.user,
                                     database = configuration.database,
                                     cursorclass = pymysql.cursors.DictCursor,
                                     charset = 'utf8mb4'
                                    )
        return connection
