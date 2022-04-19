import pytz
import os
import datetime as dt
URL_CGR = 'https://appbp.contraloria.gob.pe/BuscadorCGR/Informes/Avanzado.html#'

timezone = pytz.timezone('America/Lima')
day_before = 2
START_DATE = (dt.datetime.now(timezone) - dt.timedelta(days=day_before)).strftime('%d/%m/%Y')
END_DATE = dt.datetime.now(timezone).strftime('%d/%m/%Y')

EXECUTABLE_PATH_GECKODRIVER='/usr/local/bin/geckodriver'
EXECUTABLE_PATH_CHROMEDRIVER='D://chromedriver.exe'

PATH_OUTPUT = 'results'
os.makedirs(PATH_OUTPUT, exist_ok=True)
FILENAME_OUTPUT = 'cgr_data.json'

SALTO_DAYS = 15

# list_dict_fecha = [ {'since': '01/01/2017', 'until': '23/04/2019'},
#                     {'since': '24/04/2019', 'until': '30/05/2019'},
#                     {'since': '31/05/2019', 'until': '01/09/2019'},
#                     {'since': '02/09/2019', 'until': '15/12/2019'},
#                     {'since': '16/12/2019', 'until': '18/05/2020'},
#                     {'since': '19/05/2020', 'until': '27/08/2020'},
#                     {'since': '28/08/2020', 'until': '29/12/2020'},
#                     {'since': '30/12/2020', 'until': '11/03/2021'},
#                     {'since': '12/03/2021', 'until': '29/06/2021'},
#                     {'since': '30/06/2021', 'until': '06/09/2021'},
#                     {'since': '07/09/2021', 'until': '20/12/2021'},
#                     {'since': '21/12/2021', 'until': '12/01/2022'},
#                     {'since': '13/01/2022', 'until': '16/04/2022'} ]