import unittest
import sys
import argparse
import datetime as dt
import math
from utils import create_driver, save_json
from config import END_DATE
from extraction import SeleniumVisitas, get_visitas_last
from multiprocessing.dummy import Pool

class TestVisitas(unittest.TestCase):
    def __init__(self, **args):
        self.data = []
        self.setUp()
        self.test_visitas(**args)
        self.tearDown()
    def setUp(self) -> None:
        self.driver = create_driver(args.driver)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()
    
    def test_visitas(self, **args):
        browser = self.driver
        selenium_visita = SeleniumVisitas(browser, **args)
        self.data = selenium_visita.data
        # save_json(data)

def get_dict_fecha(since, until, salto_days):
    list_dict_fecha = []
    for i in range(0, args.pool+1):
        until_pool = since + dt.timedelta(days=salto_days)
        if until_pool>until:
            until_pool = until
            
        dict_fecha = {'since': since.strftime('%Y-%m-%d'),
                    'until': until_pool.strftime('%Y-%m-%d')}
        list_dict_fecha.append(dict_fecha)
        since = until_pool
    return list_dict_fecha

def get_visitas(dict_value):
    test_visitas = TestVisitas(**dict_value)
    return test_visitas.data

def main():

    if args.last == True:
        data = get_visitas_last()
        save_json(data)
        return None

    since = args.since
    until = args.until
    pool_size = args.pool
    pool = Pool(pool_size)

    # test_visitas = TestVisitas()
    # save_json(test_visitas.data)

    since = dt.datetime.strptime(since, '%Y-%m-%d')
    until = dt.datetime.strptime(until, '%Y-%m-%d')
    num_days = (until - since).days
    salto_days = math.floor(num_days/pool_size)

    list_dict_fecha = get_dict_fecha(since,until, salto_days)
    print('########################')
    print(list_dict_fecha)

    list_data = []
    for visitas in pool.map(get_visitas, list_dict_fecha):
        if visitas:
            list_data.extend(visitas)
    save_json(list_data)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver',
                        dest = 'driver',
                        help = 'indicar el driver a utilizar',
                        choices=['firefox','chrome'])
    parser.add_argument('--since','-s',
                        dest = 'since',
                        help = 'indicar la fecha de inicio para la extraccion, ejm 2022-05-01')
    parser.add_argument('--until', '-u',
                        dest = 'until',
                        help = 'indicar la fecha fin para la extraccion, ejm 2022-05-05',
                        default = END_DATE)
    parser.add_argument('--pool',
                        dest = 'pool',
                        help = 'indicar el numero de pool a utilizar',
                        type=int,
                        default=4)
    parser.add_argument('--last',
                        dest='last',
                        help='extraer lo ultimo',
                        action='store_true')

    args = parser.parse_args()
    main()


    
