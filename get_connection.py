#Configuration Values
import pymysql
def get_connection():
    endpoint = 'XXXXXXXXXXXXXXXXXXXXX'
    username = 'XXXXX'
    password = 'XXXXXXXXXXXXXX'
    database_name = 'XXXXXX'
    #Connection
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)
    return connection


