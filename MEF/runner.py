import argparse
from multiprocessing.dummy import Pool
import time
import pandas as pd
from utils import create_driver, save_json, load_json
from config import REGION_LIST
from extraction import SeleniumSSI, ApiDatosAbiertos
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
    ### obtener pip con la api de datos abiertos
    if args.last:
        list_response = ApiDatosAbiertos(args.region, count = 1000).list_response
        filename = f'pip_{args.region.lower()}_last.json'
        save_json(list_response, filename=filename)

    if args.all:
        list_response = ApiDatosAbiertos(args.region).list_response
        filename = f'pip_{args.region.lower()}.json'
        save_json(list_response, filename=filename)
    
    ### handling list_cui_pool
    list_cui = [str(int(i['CODIGO_UNICO'])) for i in list_response if i['CODIGO_UNICO']]
    list_cui_pool = []
    salto = len(list_cui)//n_pool
    for i in range(0, len(list_cui), salto):
        list_cui_pool.append(list_cui[i:i+salto])
    
    ## aplicar el miltiprocesamiento para extraer info del ssi
    extraction_mef_data = []
    for extraction_mef in pool.map(ExtractionMEF, list_cui_pool):
        result = extraction_mef.data 
        extraction_mef_data.extend(result)

    ### adjustar cui recolectados incorrectamente
    time.sleep(10)
    df_a = pd.DataFrame(list_response)
    df_a['CODIGO_UNICO'] = df_a['CODIGO_UNICO'].astype('int64').astype('str')
    cui_a = set(df_a['CODIGO_UNICO'])

    df_b = pd.DataFrame(extraction_mef_data)
    cui_b = set(df_b['CODIGO_UNICO'])

    cui_faltante = cui_a.difference(cui_b)
    extraction_mef = ExtractionMEF(cui_faltante)
    result = extraction_mef.data
    extraction_mef_data.extend(result)

    ### save data del ssi
    data = load_json(filename = filename)
    data_pip = {'datos_abiertos': data, 'ssi': extraction_mef_data}
    save_json(data_pip, filename = filename)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--region',
                        dest = 'region',
                        help = 'indicar la region a extraer',
                        choices = REGION_LIST)
    parser.add_argument('--last',
                        dest = 'last',
                        help = 'extraer los ultimos pip publicados',
                        action = 'store_true')
    parser.add_argument('--all',
                        dest = 'all',
                        help = 'extraer todos los pip publicados desde el 2002',
                        action = 'store_true')
    parser.add_argument('--driver',
                        dest = 'driver',
                        help = 'indicar el tipo de driver',
                        choices = ['firefox','chrome'],
                        default = 'firefox')
    parser.add_argument('--pool',
                        dest = 'pool',
                        help='indicar los numeros de hilos a utilizar',
                        type = int,
                        default=8)
    args = parser.parse_args()
    main()

