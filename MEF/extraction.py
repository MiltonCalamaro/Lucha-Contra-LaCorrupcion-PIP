from tqdm import tqdm
import time
from selenium.webdriver.common.by import By
import urllib
import requests
from config import URL_SSI, URL_MEF_API, URL_MEF, QUERY_PROYECTO, params
from utils import config, get_logger
logger = get_logger('mef')

config_yaml = config()

class ApiDatosAbiertos:

    def __init__(self, region):
        '''
        parameters
           region(str): indica el nombre de la region choices(CUSCO,LAMBAYEQUE,LORETO,LIMA,PIURA) 
        '''
        self.list_response = []
        self.params = params
        self.region = region
        # self.q = QUERY_PROYECTO[self.region]
        self.q = QUERY_PROYECTO.format(region=self.region)
        self.get_response(next_token=None)

    def get_response(self, next_token=None):
        
        if next_token is None:
            url_request = URL_MEF_API+'?'+urllib.parse.urlencode(self.params)+'&q='+self.q
        else:
            url_request = self.params['next']
        # logger.info(url_request)
        with requests.session() as s:
            response = s.get(url_request)
        response = response.json()
        ### error handling
        if response.get('error'):
            logger.warning(response['error']) 
            return None       

        if next_token is None:
            total = response['result']['total']
            logger.info(f'Existen {total} proyecto de inversion en {self.region}')

        ## records handling
        records = response['result']['records']
        if not records:
            ### cuando se llega al limite de las consultas
            logger.info(f'Se extrajeron {len(self.list_response)} proyectos de inversion')
            return None
        self.list_response.extend(records)
        logger.info(f'uploads {len(records)} records')

        ### agregar next_url
        links = response['result']['_links']
        self.params['next'] = URL_MEF + links['next']
        ### recursividad
        self.get_response(next_token=True)


class SSI:    
    QUERY_GENERAL = config_yaml['query_general']
    QUERY_EFINANCIERA = config_yaml['query_efinanciera']

    def __init__(self, browser):
        self.data = {}
        self.browser = browser
        self.get_general()
        # self.get_efinanciera()
    
    def _find_element(self, xpath):
        elem = self.browser.find_element(by=By.XPATH, value=xpath)
        elem = elem.text
        return elem

    def get_general(self):
        for xpath in self.QUERY_GENERAL:
            elem = self._find_element(self.QUERY_GENERAL[xpath])
            if elem is None:
                continue
            self.data[xpath] = elem

    def get_efinanciera(self):
        xpath_nav_item  = self.QUERY_EFINANCIERA['nav_item']
        elem = self.browser.find_element(by=By.XPATH, value=xpath_nav_item)
        elem.click()
        for xpath in self.QUERY_EFINANCIERA:
            if xpath!='nav_item':
                elem = self._find_element(self.QUERY_EFINANCIERA[xpath])
                self.data[xpath] = elem


class SeleniumSSI:
    QUERY_SEARCH = config_yaml['query_search']
    def __init__(self, browser, list_cui):
        self.data = []
        self.browser = browser
        self.search_cui(list_cui)

    def search_cui(self, list_cui):
        for cui in tqdm(list_cui):
            try:
                self.browser.get(URL_SSI)
                input_cui = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['input_cui'])
                input_cui.send_keys(cui)
                ### search cui
                search_cui = self.browser.find_element(by=By.XPATH, value=self.QUERY_SEARCH['search_cui'])
                search_cui.click()
                time.sleep(1.5)
                ### get data cui
                ssi = SSI(self.browser)
                ssi_data = ssi.data
                logger.info(f"{ssi_data['CODIGO_UNICO']} | {ssi_data['FECHA_REGISTRO']} | {ssi_data['NOMBRE_INVERSION']}")
                ### append to data
                self.data.append(ssi_data)

            except Exception as e:
                logger.warning(f"{cui}, {e}", exc_info=True)


















            