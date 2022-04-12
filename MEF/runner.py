import unittest
import argparse
import sys
import json
from multiprocessing.dummy import Pool
from utils import create_driver, save_json
from config import REGION_LIST
from extraction import SeleniumSSI, MEF_DATOSABIERTOS_API
import warnings as w
w.filterwarnings('ignore')

class ExtractionMEF:
    def __init__(self, list_cui):
        self.data = []
        self.get_data(list_cui)

    def setUp(self) -> None:
        self.driver = create_driver()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()

    def get_data(self, list_cui):
        self.setUp()
        selenium_ssi = SeleniumSSI(self.driver, list_cui)
        self.data = selenium_ssi.data
        self.tearDown()


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--region',
                        dest = 'region',
                        help = 'indicar la region a extraer',
                        choices = REGION_LIST,
                        )

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()  
 
    list_response = MEF_DATOSABIERTOS_API(args.region).list_response
    save_json(list_response, filename=f'datos_abiertos_{args.region}.json')

    list_cui = [str(int(i['CODIGO_UNICO'])) for i in list_response]


    n_pool = 10
    pool = Pool(n_pool)

    list_cui_pool = []
    salto = len(list_cui)//n_pool
    for i in range(0, len(list_cui), salto):
        list_cui_pool.append(list_cui[i:i+salto])
    
    extraction_mef_data = []
    for extraction_mef in pool.map(ExtractionMEF, list_cui_pool):
        result = extraction_mef.data 
        extraction_mef_data.extend(result)
    save_json(extraction_mef_data, filename=f'ssi_{args.region}.json')
