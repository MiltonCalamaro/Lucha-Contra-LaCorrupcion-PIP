from config import URL_SSI
from utils import config
from tqdm import tqdm
import time
from selenium.webdriver.common.by import By
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('__ssi__')

config_yaml = config()

class SSI:    
    QUERY_GENERAL = config_yaml['query_general']
    QUERY_EFINANCIERA = config_yaml['query_efinanciera']

    def __init__(self, browser):
        self.data = {}
        self.browser = browser
        self.get_general()
        self.get_efinanciera()
    
    def _find_element(self, xpath):
        elem = self.browser.find_element(by=By.XPATH, value=xpath)
        elem = elem.text
        return elem

    def get_general(self):
        for xpath in self.QUERY_GENERAL:
            elem = self._find_element(self.QUERY_GENERAL[xpath])
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
                time.sleep(2)
                ### get data cui
                ssi = SSI(self.browser)
                ssi_data = ssi.data
                logging.info(f"{ssi_data['cui']} | {ssi_data['fecha_registro']} | {ssi_data['nombre_inversion']}")
                ### append to data
                self.data.append(ssi_data)

            except Exception as e:
                logging.warning(f"{cui}, {e}", exc_info=True)


















            