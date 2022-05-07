import mysql.connector as mysql
import pandas as pd

def query():
    con = mysql.connect(host = 'db-dsrp-dev.cdykihpovon2.us-east-1.rds.amazonaws.com',
                        port = '3306',
                        user = 'admin',
                        database = 'dsrp',
                        password = 't8P2uEeRHsiDnCEDaaRE'
                    )

    query_sector = """
    select DISTINCT NomSec from dsrp.tabla_sector ts 
    """
    df = pd.read_sql(query_sector, con)
    df['NomSec'] = df['NomSec'].str.rstrip()
    res = df.to_json(orient='records')
    return res
