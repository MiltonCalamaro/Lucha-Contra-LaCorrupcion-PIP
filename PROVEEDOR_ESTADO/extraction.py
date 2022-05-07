import time
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils import config, get_logger 
from config import URL_PERFILPROV
logger = get_logger('proveedores_estado')

class SeleniumProveedor:
    QUERY_SEARCH = config()['query_search']
    QUERY_ANTECEDENTES = config()['query_antecedentes']
    QUERY_PROVEEDOR = config()['query_proveedor']

    def __init__(self, browser, list_ruc):
        self.data = []
        self.browser = browser
        self.get_proveedores(list_ruc)

    def _find_element(self, xpath, text=False):
        elem = self.browser.find_element(by=By.XPATH, value=xpath)
        if text==True:
            elem = elem.text
        return elem

    def _check_resultado(self):
        elem_resultado = self._find_element(self.QUERY_SEARCH['resultado'])
        if  elem_resultado.text.strip() =='No se encontró resultados':
            return False
        return True

    def _get_antecedentes(self):
        dict_antecedentes  = {}
        for key, value in self.QUERY_ANTECEDENTES.items():
            dict_antecedentes[key] = self._find_element(value, text=True)
        return dict_antecedentes

    def _get_proveedor(self):
        dict_proveedor = {}
        for key, value in self.QUERY_PROVEEDOR.items():
            dict_proveedor[key] = self._find_element(value, text=True)
        return dict_proveedor

    def _search_proveedores(self, ruc):
        self.browser.get(URL_PERFILPROV)
        
        elem_input = self._find_element(self.QUERY_SEARCH['input']) 
        elem_input.send_keys(ruc)

        elem_buscar = self._find_element(self.QUERY_SEARCH['buscar']) 
        elem_buscar.click()

        if self._check_resultado():
            elem_proveedor = self._find_element(self.QUERY_SEARCH['proveedor'])
            elem_proveedor.click()
            elem_vermas = self._find_element(self.QUERY_SEARCH['vermas'])
            elem_vermas.click()
            
            time.sleep(2)
            dict_antecedentes = self._get_antecedentes()
            time.sleep(2)
            dict_proveedor = self._get_proveedor()

            # dict_result = {'proveedor': dict_proveedor , 'antecedentes': dict_antecedentes}
            dict_proveedor.update(dict_antecedentes)
            logger.info(f"{dict_proveedor['ruc']} | {dict_proveedor['nombre']} | {dict_proveedor['estado']}")
            return dict_proveedor

        logger.info(f'No hay informacion del proveedor con ruc {ruc}')
        return None

    def get_proveedores(self, list_ruc):
        
        for ruc in tqdm(list_ruc):
            try:
                dict_result = self._search_proveedores(ruc)
                if dict_result:
                    self.data.append(dict_result)
            except Exception  as e:
                logger.warning(f"error {ruc}, {e}")
