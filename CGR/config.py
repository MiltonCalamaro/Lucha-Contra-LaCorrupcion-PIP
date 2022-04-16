import pytz
import os
import datetime as dt
URL_CGR = 'https://appbp.contraloria.gob.pe/BuscadorCGR/Informes/Avanzado.html#'

timezone = pytz.timezone('America/Lima')
day_before = 7
START_DATE = (dt.datetime.now(timezone) - dt.timedelta(days=day_before)).strftime('%d/%m/%Y')
END_DATE = dt.datetime.now(timezone).strftime('%d/%m/%Y')

EXECUTABLE_PATH_GECKODRIVER='/usr/local/bin/geckodriver'
EXECUTABLE_PATH_CHROMEDRIVER='D://chromedriver.exe'

PATH_OUTPUT = 'results'
os.makedirs(PATH_OUTPUT, exist_ok=True)
FILENAME_OUTPUT = 'cgr_data.json'