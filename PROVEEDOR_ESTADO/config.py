import os
import pytz
import datetime as dt
from fake_useragent import UserAgent

EXECUTABLE_PATH_GECKODRIVER='/usr/local/bin/geckodriver'
EXECUTABLE_PATH_CHROMEDRIVER='D://chromedriver.exe'

URL_PERFILPROV = "https://apps.osce.gob.pe/perfilprov-ui"

PATH_OUTPUT = 'results'
os.makedirs(PATH_OUTPUT, exist_ok=True)
FILENAME_OUTPUT = 'proveedores_estado.json'
