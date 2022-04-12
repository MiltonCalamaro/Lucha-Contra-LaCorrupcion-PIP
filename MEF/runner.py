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
        self.driver = create_driver(args.driver)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()

    def get_data(self, list_cui):
        self.setUp()
        selenium_ssi = SeleniumSSI(self.driver, list_cui)
        self.data = selenium_ssi.data
        self.tearDown()

def main():
    ### configurar pool multiprocessing
    n_pool = args.pool
    pool = Pool(n_pool)

    ### obtener detalle de proyectos de inversion
    list_response = MEF_DATOSABIERTOS_API(args.region).list_response
    save_json(list_response, filename=f'datos_abiertos_{args.region}.json')
    
    ### handling list_cui_pool
    list_cui = [str(int(i['CODIGO_UNICO'])) for i in list_response]
    list_cui_pool = []
    salto = len(list_cui)//n_pool
    for i in range(0, len(list_cui), salto):
        list_cui_pool.append(list_cui[i:i+salto])
    
    ### aplicar el miltiprocesamiento
    extraction_mef_data = []
    for extraction_mef in pool.map(ExtractionMEF, list_cui_pool):
        result = extraction_mef.data 
        extraction_mef_data.extend(result)
    save_json(extraction_mef_data, filename=f'ssi_{args.region}.json')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--region',
                        dest = 'region',
                        help = 'indicar la region a extraer',
                        choices = REGION_LIST,
                        )

    parser.add_argument('--driver',
                        dest = 'driver',
                        help = 'indicar el tipo de driver',
                        choices = ['firefox','chrome'],
                        )
    parser.add_argument('--pool',
                        dest = 'pool',
                        help='indicar el numeros de hilos multiprocesos a ejecutar',
                        type = int,
                        default=10)

    args = parser.parse_args()
    main()

