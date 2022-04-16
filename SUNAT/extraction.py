import logging
import requests
import time
from tqdm import tqdm
import warnings as w
w.filterwarnings('ignore')
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from config import URL_RUC, URL_RUC_API, headers, params
from utils import config, get_logger

config_yaml = config()
logger = get_logger('ruc')

class RucApi:
    def __init__(self, ruc):
        self.ruc = ruc
        self.response = {}
        self.get_response()

    def get_response(self):

        with requests.session() as s:
            params['ruc'] = self.ruc
            s.headers = headers
            response = s.request(method='POST', url=URL_RUC_API, params=params) 
        response = response.json()  
        
        if response.get('error'):
            logger.warning(f"{self.ruc} , {response['error']}")
            return None

        logger.info(f"{response['ruc']} | {response['nombre_o_razon_social']}")
        self.response = response

class RucScrapy:
    QUERY_INFO = config_yaml['query_info']

    def __init__(self, browser):
        self.data = {}
        self.browser = browser
        self.get_features()

    def _get_html(self):
        html = BeautifulSoup(self.browser.page_source, 'html.parser')
        return html

    def _find_element(self, xpath):
        elem = self.browser.find_element(by=By.XPATH, value=xpath)
        elem = elem.text
        return elem

    def get_features(self):
        html = self._get_html()
        if not html.select_one(self.QUERY_INFO['check_ruc']):
            logger.warning('No existe Número de RUC')
            return None

        for xpath in  self.QUERY_INFO['fields']:
            elem = self._find_element(self.QUERY_INFO['fields'][xpath])
            self.data[xpath] = elem

class RLegales:
    QUERY_RLEGALES = config_yaml['query_rlegales']

    def __init__(self, browser):
        self.list_data = []
        self.browser = browser
        self.get_rlegales()

    def _get_html(self):
        html = BeautifulSoup(self.browser.page_source, 'html.parser')
        return html

    def _click_rlegales(self):
        ### validar si existe Representante(s) Legal(es)
        html = self._get_html()
        if not html.select_one(self.QUERY_RLEGALES['check_rl']):
            logger.warning('No existe Representante(s) Legal(es)')
            return None
        ### click Representante(s) Legal(es)    
        elem = self.browser.find_element(by=By.XPATH, value=self.QUERY_RLEGALES['buscar'])
        self.browser.execute_script('arguments[0].click();',elem)
        html = self._get_html()
        return html

    def _find_element(self, table_tr, selector):
        elem = table_tr.select_one(selector)
        elem = elem.text
        return elem

    def get_rlegales(self):
        html = self._click_rlegales()
        if not html:
            return None
        ## encontrar los representantes legales
        for table_tr in html.select(self.QUERY_RLEGALES['table_tr']):
            dict_data = {}
            ## iterar por cada selector para extraer del registro
            for selector in self.QUERY_RLEGALES['fields']:
                dict_data[selector] = self._find_element(table_tr, self.QUERY_RLEGALES['fields'][selector])
            self.list_data.append(dict_data)

class SeleniumRuc:
    QUERY_SEARCH  = config_yaml['query_search']
    
    def __init__(self, browser, list_ruc):
        self.data = []
        self.browser = browser
        self.search_browser(list_ruc)

    def search_browser(self, list_ruc):
        logger.info('STARTING SCRAPER RUC')
        for ruc in tqdm(list_ruc):
            try:
                ### ingresar url
                self.browser.get(URL_RUC)
                time.sleep(5)
                ### input ruc
                logger.info(f'{"#"*50}')
                logger.info('Ingresar RUC {ruc}'.format(ruc=ruc))
                input_ruc = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['input'])
                input_ruc.send_keys(ruc)
                time.sleep(5)
                ### search ruc
                logger.info('Buscar RUC')
                button_buscar = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['buscar'])
                button_buscar.click()
                time.sleep(5)
                ### get features ruc
                logger.info('Obtener datos RUC')
                dict_data  = RucScrapy(self.browser).data
                if not dict_data:
                    continue
                time.sleep(5)
                ### get representantes legales
                logger.info('Representante(s) Legal(es)')
                r_legales = RLegales(self.browser).list_data
                ### add representantes legales
                dict_data['r_legales'] = r_legales
                self.data.append(dict_data)
                ### return homepage
                # button_regresar = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['regresar'])
                # button_regresar.click()
            except Exception as e:
                logger.warning(f'error in {ruc}')
                pass
        logger.info('FINISHING SCRAPER RUC')


