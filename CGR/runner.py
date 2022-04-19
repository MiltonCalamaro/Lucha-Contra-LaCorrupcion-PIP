import argparse
import datetime as dt
import math
import logging
from multiprocessing.dummy import Pool
from utils import create_driver, save_json
from config import END_DATE, SALTO_DAYS
from extraction import SeleniumCGR

class ExtractionCGR:
    def __init__(self, **args):
        self.data = [] 
        self.setUp()
        self.get_cgr(**args)
        self.tearDown()

    def setUp(self) -> None:
        self.driver = create_driver(args.driver)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()
    
    def get_cgr(self, **args):
        browser = self.driver
        selenium_cgr = SeleniumCGR(browser, **args)
        self.data = selenium_cgr.data

def dividir_fecha(since, until, salto_days):
    '''
    Dividir la fecha en un rango de salto_days
    return: list of dict 
    '''
    list_dict_fecha = []
    if since < dt.datetime(2018, 12, 31):
        dict_fecha = {'since': since.strftime('%d/%m/%Y'),
                            'until': '31/12/2018'}
        list_dict_fecha.append(dict_fecha)
        since = dt.datetime(2019, 1, 1)
        
    until_pool = since
    sw = True
    while sw:
        until_pool = since + dt.timedelta(days=salto_days)
        if until_pool >= until:
           until_pool = until
           sw = False
        if since == until_pool:
            break
        dict_fecha = {'since': since.strftime('%d/%m/%Y'),
                     'until': until_pool.strftime('%d/%m/%Y')}
        list_dict_fecha.append(dict_fecha)
        since = until_pool + dt.timedelta(days=1)
    return list_dict_fecha 

def get_cgr(dict_value):
    extraction_cgr = ExtractionCGR(**dict_value)
    return extraction_cgr.data

def main():
    if args.last==True:
        extraction_cgr = ExtractionCGR()
        save_json(extraction_cgr.data, 'informes_cgr_last.json')
        return None

    pool_size = args.pool
    pool = Pool(pool_size)
    since = args.since
    until = args.until

    since = dt.datetime.strptime(since, '%Y-%m-%d')
    until = dt.datetime.strptime(until, '%d/%m/%Y')
    list_dict_fecha = dividir_fecha(since,until, SALTO_DAYS)
    logging.info(list_dict_fecha)

    list_data = []
    for cgr in pool.map(get_cgr, list_dict_fecha):
        list_data.extend(cgr)
    save_json(list_data, 'informes_cgr.json')

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--last',
                        dest = 'last',
                        help = 'Activar la opcion de extraer los ultimos reportes',
                        action = 'store_true')
    parser.add_argument('--since',
                        dest = 'since',
                        help = 'Especificar fecha de inicio de extraccion de la forma %Y-%m-%d')
    parser.add_argument('--until',
                        dest = 'until',
                        help = 'Especificar fecha final de extraccion de la forma %Y-%m-%d',
                        default=END_DATE)
    parser.add_argument('--driver',
                        dest = 'driver',
                        help = 'Indicar el driver a utilizar',
                        choices = ['firefox','chrome'],
                        default = 'firefox')
    parser.add_argument('--pool',
                        dest = 'pool',
                        help = 'Especificar el numero de hilos a utilizar',
                        type = int,
                        default = 8)
    args = parser.parse_args()
    main()
