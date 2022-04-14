import time
import re
import math
from multiprocessing.dummy import Pool
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import config, get_logger
from config import URL_CGR, START_DATE
import sys
sys.setrecursionlimit(2000)

regex = re.compile(r'Total:\s+(\d+)')
config_yaml = config()
logger = get_logger('CGR')
pool = Pool(25)


class InformesCGR:
    QUERY_TABLE = config_yaml['query_table']
    
    def __init__(self, html):
        self.informes = []
        self.html = html
        self.get_informes()

    def _get_features(self, tr):
        dict_data = {}
        for item in self.fields:
            dict_data[item] = tr.select_one(self.fields[item])
            if 'link' not in item:
                if dict_data[item]:
                    dict_data[item]  = dict_data[item].get_text().strip()
            else:
                if dict_data[item] and dict_data[item].get('href'):
                    dict_data[item] = dict_data[item].get('href').strip()   
        return dict_data

    def get_informes(self):
        table = self.QUERY_TABLE['table']
        list_tr = self.html.select(table)
        self.fields = self.QUERY_TABLE['fields']
        for dict_data in pool.map(self._get_features, list_tr):
            self.informes.append(dict_data)

class SeleniumCGR:
    QUERY_SEARCH = config_yaml['query_search']
    counter = 0
    MAX_ATTEMPS = 0

    def __init__(self, browser):
        self.data = []
        self.browser = browser
        self.browser.get(URL_CGR)
        self.get_filters()
        self.show_more()
        self.get_nro_registros()
        self.search_informes()

    def _click_element(self, xpath):
        elem = self.browser.find_element(by=By.XPATH, value = xpath)
        elem.click()
    
    def get_filters(self):
        for xpath in (self.QUERY_SEARCH['filters'] or []):
            self._click_element(self.QUERY_SEARCH['filters'][xpath])
        # fecha_desde = self.browser.find_element(by = By.XPATH, value = self.QUERY_SEARCH['fecha_desde'])
        # fecha_desde.send_keys(START_DATE)
        # buscar = self.browser.find_element(by = By.XPATH, value =  self.QUERY_SEARCH['buscar'])
        # buscar.click()

    def get_nro_registros(self):
        total_registros = self.browser.find_element(by=By.XPATH, value = self.QUERY_SEARCH['total_registros'])
        nro_registros = regex.search(total_registros.text).group(1)
        self.MAX_ATTEMPS = math.ceil(int(nro_registros)/100)

    def show_more(self):
        combo_box = self.browser.find_element(by=By.XPATH, value = self.QUERY_SEARCH['combo_box'])
        combo_box.send_keys(Keys.ENTER)
        time.sleep(3)
        option_100 = self.browser.find_element(by=By.XPATH, value = self.QUERY_SEARCH['option_100'])
        option_100.click()

    def search_informes(self):
        try:        
            html = BeautifulSoup(self.browser.page_source, 'html.parser')
            informe_cgr = InformesCGR(html)

            logger.info(f'uploads {len(informe_cgr.informes)}, iteracion {self.counter+1}')
            self.data.extend(informe_cgr.informes)

            self.counter+=1
            if self.MAX_ATTEMPS==self.counter:
                return None

            siguiente =self.browser.find_element(by = By.XPATH, value = self.QUERY_SEARCH['siguiente'])
            siguiente.click()
            # time.sleep(1)
            self.search_informes()
        except Exception as e:
            logger.warning(e)
