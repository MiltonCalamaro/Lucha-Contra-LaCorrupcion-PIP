import sys
import argparse
import datetime as dt
import math
import logging
from multiprocessing.dummy import Pool
from utils import create_driver, save_json
from config import END_DATE
from extraction import SeleniumVisitas, VisitaPresidencia, VisitaCongreso

class TestVisitas:
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

def dividir_fecha_presidencia(since, until, salto_days):
    list_dict_fecha = []
    for i in range(0, args.pool+1):
        until_pool = since + dt.timedelta(days=salto_days)
        if until_pool>=until:
            until_pool = until
        dict_fecha = {'since': since.strftime('%Y-%m-%d'),
                      'until': until_pool.strftime('%Y-%m-%d')}
        if since >=until:
            break
        list_dict_fecha.append(dict_fecha)
        since = until_pool  + dt.timedelta(days=1)
    return list_dict_fecha

def dividir_fecha_congreso(since, until, salto_days):
    sw = True
    list_dict_fecha = []
    while sw:
        until_rec =since + dt.timedelta(days=salto_days)
        if until_rec >= until:
            until_rec = until
            sw = False
        dict_fecha = {'since': since.strftime('%Y-%m-%d'),
                      'until': until_rec.strftime('%Y-%m-%d')}
        list_dict_fecha.append(dict_fecha)
        since = until_rec + dt.timedelta(days=1)
    return list_dict_fecha


def get_visitas(dict_value):
    test_visitas = TestVisitas(**dict_value)
    return test_visitas.data

def main():
    if args.poder=='congreso':
        if args.last == True:
            visita_congreso = VisitaCongreso()
            save_json(visita_congreso.data, filename='visita_congreso_last.json')
            return None

        since = args.since
        until = args.until

        since = dt.datetime.strptime(since, '%Y-%m-%d')
        until = dt.datetime.strptime(until, '%Y-%m-%d')
        salto_days = 30

        list_fecha = dividir_fecha_congreso(since, until, salto_days)
        list_data = []
        for dict_fecha in list_fecha:
            visita_congreso = VisitaCongreso(**dict_fecha)
            list_data.extend(visita_congreso.data)
        save_json(list_data,'visita_congreso.json')


    if args.poder=='presidencia':
        if args.last == True:
            visita_presidencia = VisitaPresidencia()
            save_json(visita_presidencia.data, 'visita_presidencia_last.json')
            return None

        since = args.since
        until = args.until
        pool_size = args.pool
        pool = Pool(pool_size)

        since = dt.datetime.strptime(since, '%Y-%m-%d')
        until = dt.datetime.strptime(until, '%Y-%m-%d')
        num_days = (until - since).days
        salto_days = math.floor(num_days/pool_size)
        if salto_days == 0:
            salto_days = 1

        list_fecha = dividir_fecha_presidencia(since, until, salto_days)
        logging.info(list_fecha)
        
        list_data = []
        for visitas in pool.map(get_visitas, list_fecha):
            if visitas:
                list_data.extend(visitas)
        save_json(list_data, 'visita_presidencia.json')


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver',
                        dest = 'driver',
                        help = 'indicar el driver a utilizar',
                        choices = ['firefox','chrome'],
                        default = 'firefox')

    parser.add_argument('--pool',
                        dest = 'pool',
                        help = 'indicar el numero de pool a utilizar',
                        type=int,
                        default=16)

    parser.add_argument('--since','-s',
                        dest = 'since',
                        help = 'indicar la fecha de inicio para la extraccion, ejm 2022-05-01')

    parser.add_argument('--until', '-u',
                        dest = 'until',
                        help = 'indicar la fecha fin para la extraccion, ejm 2022-05-05',
                        default = END_DATE)

    parser.add_argument('--last',
                        dest='last',
                        help='extraer lo ultimo',
                        action='store_true')

    parser.add_argument('--poder',
                        dest='poder',
                        help='indicar el poder del estado a extraer sus visitas',
                        choices=['congreso','presidencia'])

    args = parser.parse_args()
    main()


    
