import unittest
import sys
import argparse
import datetime as dt
import math
import logging
from multiprocessing.dummy import Pool
from utils import create_driver, save_json
from config import END_DATE
from extraction import SeleniumCGR

class TestCGR:
    def __init__(self, **args):
        self.data = [] 
        self.setUp()
        self.test_cgr(**args)
        self.tearDown()

    def setUp(self) -> None:
        self.driver = create_driver(args.driver)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()
    
    def test_cgr(self, **args):
        browser = self.driver
        selenium_cgr = SeleniumCGR(browser, **args)
        self.data = selenium_cgr.data

def get_dict_fecha(since, until):
    list_dict_fecha = []
    if since < dt.datetime(2018, 12, 31):
        dict_fecha = {'since': since.strftime('%d/%m/%Y'),
                            'until': '31/12/2018'}
        list_dict_fecha.append(dict_fecha)
        since = dt.datetime(2019, 1, 1)
        
    salto_days = 15
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
    test_cgr = TestCGR(**dict_value)
    return test_cgr.data

def main():
    if args.last==True:
        test_cgr = TestCGR()
        save_json(test_cgr.data, 'informes_cgr_last.json')
        return None

    pool_size = args.pool
    pool = Pool(pool_size)

    since = args.since
    since = dt.datetime.strptime(since, '%Y-%m-%d')
    until = dt.datetime.strptime(END_DATE, '%d/%m/%Y')

    list_dict_fecha = get_dict_fecha(since,until)
    logging.info(list_dict_fecha)

    list_data = []
    for cgr in pool.map(get_cgr, list_dict_fecha):
        if cgr:
            list_data.extend(cgr)
    save_json(list_data, 'informes_cgr.json')

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver',
                        dest = 'driver',
                        help = 'indicar el driver a utilizar',
                        choices=['firefox','chrome'],
                        default='firefox')
    parser.add_argument('--since',
                        dest = 'since',
                        help='indicar la fecha inicio de extracion'
                        )
    parser.add_argument('--pool',
                        dest = 'pool',
                        help='indicar los nro de pool para el multiprocesamiento',
                        type = int,
                        default = 16)
    parser.add_argument('--last',
                        dest = 'last',
                        help = 'activar la opcion de extraer los ultimos',
                        action = 'store_true')
    args = parser.parse_args()
    main()
