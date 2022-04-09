import logging
import requests
import time
from tqdm import tqdm
import warnings as w
from selenium.webdriver.common.by import By
# from config import dict_features, xpath_input, xpath_buscar, xpath_regresar
from config import URL_RUC, URL_RUC_API, headers, params
from utils import config

config_yaml = config()
w.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('__ruc__')

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

    def _find_element(self, xpath):
        elem = self.browser.find_element(by=By.XPATH, value=xpath)
        elem = elem.text
        return elem

    def get_features(self):
        for xpath in self.QUERY_INFO:
            elem = self._find_element(self.QUERY_INFO[xpath])
            self.data[xpath] = elem

class SeleniumRuc:
    QUERY_SEARCH  = config_yaml['query_search']
    
    def __init__(self, browser, list_ruc):
        self.data = []
        self.browser = browser
        self.search_browser(list_ruc)

    def search_browser(self, list_ruc):
        self.browser.get(URL_RUC)
        time.sleep(3)        
        logger.info('STARTING SCRAPER RUC')
        for ruc in tqdm(list_ruc):
            try:
                ### input ruc
                time.sleep(3)
                input_ruc = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['input'])
                input_ruc.send_keys(ruc)
                ### search ruc
                button_buscar = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['buscar'])
                button_buscar.click()
                time.sleep(7)
                ### get features ruc
                dict_data  = RucScrapy(self.browser).data
                if dict_data:
                    self.data.append(dict_data) 
                ### return homepage
                button_regresar = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['regresar'])
                button_regresar.click()
                time.sleep(5)
            except Exception as e:
                logger.warning(f'error in {ruc} , {e}', exc_info=True)
                self.browser.get(URL_RUC)
        logger.info('FINISHING SCRAPER RUC')


