#Configuration Values
import pymysql
def get_connection():
    endpoint = 'db-dsrp-dev.cdykihpovon2.us-east-1.rds.amazonaws.com'
    username = 'admin'
    password = 't8P2uEeRHsiDnCEDaaRE'
    database_name = 'dsrp'
    #Connection
    connection = pymysql.connect(host=endpoint, user=username, passwd=password, db=database_name)
    return connection


