import logging
import requests
import time
from tqdm import tqdm
import warnings as w
from selenium.webdriver.common.by import By
from config import dict_features, xpath_input, xpath_buscar, xpath_regresar
from config import URL_RUC, URL_RUC_API, headers, params

w.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('__ruc__')

class RucApi:
    def __init__(self, ruc):
        self.ruc = ruc
        self.data = {}
        self._get_features()

    def _get_features(self):

        with requests.session() as s:
            params['ruc'] = self.ruc
            s.headers = headers
            response = s.request(method='POST', url=URL_RUC_API, params=params) 
        data = response.json()  
        
        if data.get('error'):
            logger.warning(f"{self.ruc} , {data['error']}")
            return None

        logger.info(f"{data['ruc']} | {data['nombre_o_razon_social']}")
        self.data = data

class NroRuc:
    def __init__(self, browser):
        self.data = {}
        self.browser = browser
        self._get_features()

    def _get_features(self):
        for feature in dict_features:
            elem = self.browser.find_element(by=By.XPATH, value=dict_features[feature])
            self.data[feature]=elem.text

class SeleniumRuc:
    def __init__(self, browser, list_ruc):
        self.data = []
        self.browser = browser
        self.browser.get(URL_RUC)
        time.sleep(5)
        self.search_browser(list_ruc)

    def search_browser(self, list_ruc):        
        logger.info('STARTING SCRAPER RUC')
        for ruc in tqdm(list_ruc):
            try:
                ### input ruc
                time.sleep(3)
                input_ruc = self.browser.find_element(by=By.XPATH, value=xpath_input)
                input_ruc.send_keys(ruc)
                ### search ruc
                button_buscar = self.browser.find_element(by=By.XPATH, value=xpath_buscar)
                button_buscar.click()
                time.sleep(7)
                ### get features ruc
                dict_data  = NroRuc(self.browser).data
                if dict_data:
                    self.data.append(dict_data)
                ### return homepage
                button_regresar = self.browser.find_element(by=By.XPATH, value=xpath_regresar)
                button_regresar.click()
                time.sleep(5)
            except Exception as e:
                logger.warning(f'error in {ruc} , {e}', exc_info=True)
                self.browser.get(URL_RUC)
        logger.info('FINISHING SCRAPER RUC')


