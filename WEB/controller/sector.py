import mysql.connector as mysql
import pandas as pd

def query():
    con = mysql.connect(host = 'XXXXXXXXXXXXX',
                        port = 'XXXXX',
                        user = 'XXXXXXX',
                        database = 'XXXXXXXXXX',
                        password = 'XXXXXXX'
                    )

    query_sector = """
    select DISTINCT NomSec from dsrp.tabla_sector ts 
    """
    df = pd.read_sql(query_sector, con)
    df['NomSec'] = df['NomSec'].str.rstrip()
    res = df.to_json(orient='records')
    return res
