import os
import pytz
import datetime as dt
from fake_useragent import UserAgent

EXECUTABLE_PATH_GECKODRIVER='/usr/local/bin/geckodriver'
EXECUTABLE_PATH_CHROMEDRIVER='D://chromedriver.exe'

# URL_CONGRESO = 'https://wb2server.congreso.gob.pe/regvisitastransparencia/#'
URL_CONGRESO_API = 'https://wb2server.congreso.gob.pe/regvisitastransparencia/filtrar'
URL_PRESIDENCIA = 'https://appw.presidencia.gob.pe/visitas/transparencia/'

PATH_OUTPUT = 'results'
os.makedirs(PATH_OUTPUT, exist_ok=True)
FILENAME_OUTPUT = 'visita.json'

timezone = pytz.timezone('America/Lima')
day_before = 2
START_DATE = (dt.datetime.now(timezone) - dt.timedelta(days=day_before)).strftime('%Y-%m-%d')
END_DATE = dt.datetime.now(timezone).strftime('%Y-%m-%d')

DICT_MONTH = {'1':'Ene','2':'Feb','3':'Mar', '4':'Abr', '5':'May', '6':'Jun','7':'Jul',
             '8':'Ago','9':'Sep','10':'Oct','11':'Nov','12':'Dic'}

user_agent  = UserAgent().chrome
HEADERS = {'headers':user_agent}

SALTO_DAYS_CONGRESO = 30
