import time
import datetime as dt
import re
import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from utils import config, get_logger
from config import START_DATE, END_DATE, URL_PRESIDENCIA, DICT_MONTH

user_agent  = UserAgent().chrome
regex = re.compile(r'(\d+)\s+\w+')
config_yaml = config()
logger = get_logger('visitas_presidencia')

class VisitaPresidencia:
    QUERY_SELECTOR = config_yaml['query_selector']

    def __init__(self, html):
        self.data = []
        self.html = html
        self.get_fields()

    def get_fields(self):
        table_tr = self.html.select(self.QUERY_SELECTOR['table_tr'])
        fields = self.QUERY_SELECTOR['fields']
        for tr in table_tr[1:]:
            dict_data = {}
            for item in fields:
                dict_data[item] = tr.select_one(fields[item])
                dict_data[item] = dict_data[item].text.strip()
            self.data.append(dict_data)

def get_visitas_last():
    response = requests.get(URL_PRESIDENCIA, headers={'headers':user_agent})
    if response.status_code==200:
        html = BeautifulSoup(response.content, 'html.parser')
        visitas_presidencia = VisitaPresidencia(html)
        return visitas_presidencia.data
    return None


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
            show_calendary = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['show_calendary'])
            show_calendary.send_keys('')
            time.sleep(1)
            # logger.info(f"buscando {self.since.strftime('%Y-%m-%d')}")
            
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
            str_since  = self.since.strftime('%Y-%m-%d')

            html = BeautifulSoup(self.browser.page_source, 'html.parser')
            number_register = html.select_one(self.QUERY_SEARCH['check_register'])
            if number_register and regex.search(number_register.text):
                number_register = regex.search(number_register.text).group(1)
                visita_presidencia = VisitaPresidencia(html).data
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
