import time
import datetime as dt
import re
import requests
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

from utils import config, get_logger
from config import START_DATE, END_DATE, URL_PRESIDENCIA, DICT_MONTH, URL_CONGRESO_API, HEADERS

regex = re.compile(r'(\d+)\s+\w+')
config_yaml = config()
logger = get_logger('visitas')

class VisitaCongreso:
    def __init__(self, since=START_DATE, until=END_DATE):
        self.data = []
        self.since = since
        self.until = until
        self.get_response()

    def _config_auth_data(self):
        dt_since =dt.datetime.strptime(self.since,'%Y-%m-%d')
        dt_until =dt.datetime.strptime(self.until,'%Y-%m-%d')
        if (dt_until - dt_since).days >30:
            logger.warning('la diferencia de fecha  no debe exceder 30 dias')
            return None
        auth_data = {"fechaDesde":self.since,
                     "fechaHasta":self.until}
        return auth_data
    
    def get_response(self):
        auth_data = self._config_auth_data()
        if auth_data:
            response = requests.post(URL_CONGRESO_API, data=json.dumps(auth_data), headers=HEADERS).json()
            logger.info(f'{self.since} - {self.until} , extrayendo {len(response)}')
            self.data = response
            

class VisitaPresidencia:
    QUERY_SELECTOR = config_yaml['query_selector']

    def __init__(self, html=None):
        self.data = []
        self.html = html
        self.get_fields()

    def _get_html(self):
        response = requests.get(URL_PRESIDENCIA, headers=HEADERS)
        if response.status_code==200:
            self.html = BeautifulSoup(response.content, 'html.parser')
        else:
            logger.info('error status_code not equal 200')
            
    def get_fields(self):
        if not self.html:
            self._get_html()
        table_tr = self.html.select(self.QUERY_SELECTOR['table_tr'])
        fields = self.QUERY_SELECTOR['fields']
        for tr in table_tr[1:]:
            dict_data = {}
            for item in fields:
                dict_data[item] = tr.select_one(fields[item])
                dict_data[item] = dict_data[item].text.strip()
            self.data.append(dict_data)

        
class SeleniumVisitas:
    QUERY_SEARCH = config_yaml['query_search']
    counter = 0

    def __init__(self, browser, since = START_DATE, until = END_DATE):
        self.data = []
        self.browser = browser
        self.since = since
        self.until = until
        self.browser.get(URL_PRESIDENCIA)
        time.sleep(3)
        self.calculate_days()
        self.get_search_visitas()

    def calculate_days(self):
        self.since = dt.datetime.strptime(self.since, "%Y-%m-%d")
        self.until = dt.datetime.strptime(self.until, "%Y-%m-%d")
        self.num_days = (self.until - self.since).days
        logger.info(f"periodo: {self.since.strftime('%Y-%m-%d')} - {self.until.strftime('%Y-%m-%d')} | numero dias {self.num_days}")

    def get_search_visitas(self):
        try:
            if self.since > self.until:
                return None

            str_since  = self.since.strftime('%Y-%m-%d')
            show_calendary = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['show_calendary'])
            show_calendary.send_keys('')
            time.sleep(1)
            
            since_year = str(self.since.year)
            since_month = DICT_MONTH[str(self.since.month)]
            since_day = str(self.since.day)

            xpath_year =self.QUERY_SEARCH['year'].format(year=since_year)
            year = self.browser.find_element(by=By.XPATH, value=xpath_year)
            year.click()
            time.sleep(3)

            xpath_month =self.QUERY_SEARCH['month'].format(month=since_month)
            month = self.browser.find_element(by=By.XPATH, value=xpath_month)
            month.click()
            time.sleep(3)

            xpath_day =self.QUERY_SEARCH['day'].format(day=since_day)
            day = self.browser.find_element(by=By.XPATH, value=xpath_day)
            day.click()
            time.sleep(3)

            search = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['search'])
            search.click()
            time.sleep(3)

            ### check register
            html = BeautifulSoup(self.browser.page_source, 'html.parser')
            number_register = html.select_one(self.QUERY_SEARCH['check_register'])
            if number_register and regex.search(number_register.text):
                number_register = regex.search(number_register.text).group(1)
                visita_presidencia = VisitaPresidencia(html)
                visita_presidencia = visita_presidencia.data
                logger.info(f'{str_since} | registro total {number_register} ,  scrapeados {len(visita_presidencia)}')      

                self.data.extend(visita_presidencia)
            else:
                logger.warning(f"{str_since} | not register founded")
            
            if self.counter==self.num_days:
                return None

            self.since = self.since + dt.timedelta(days=1)
            self.counter+=1

        except Exception as e:
            logger.warning(f"error, {str_since}")

        self.get_search_visitas()
