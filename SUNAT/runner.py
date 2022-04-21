import argparse
import sys
import json
from os.path import basename
from extraction import SeleniumRuc, RucApi
from utils import create_driver, save_json
from multiprocessing.dummy import Pool
import warnings as w
w.filterwarnings('ignore')

class TestSeleniumRUC:
    def __init__(self, list_ruc):
        self.data = []
        self.setUp()
        self.test_selenium_ruc(list_ruc)
        self.tearDown()

    def setUp(self) -> None:
        self.driver = create_driver(args.driver)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()

    def test_selenium_ruc(self, list_ruc):
        browser = self.driver
        selenium_ruc = SeleniumRuc(browser, list_ruc)
        self.data = selenium_ruc.data


def main():
    n_pool = args.pool
    pool = Pool(n_pool)

    with open(args.ruc, mode='r', encoding='utf-8') as f:
        list_ruc = json.load(f)

    list_ruc_pool = []
    salto = len(list_ruc)//n_pool
    for i in range(0, len(list_ruc), salto):
        list_ruc_pool.append(list_ruc[i:i+salto])

    extraction_ruc_data = []
    for extraction_ruc in pool.map(TestSeleniumRUC, list_ruc_pool):
        result = extraction_ruc.data
        extraction_ruc_data.extend(result)
    save_json(extraction_ruc_data, basename(args.ruc))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--ruc','-r',
                        dest = 'ruc',
                        help = 'indicar la lista de ruc a extraer')
    parser.add_argument('--driver',
                        dest = 'driver',
                        help = 'indicar el driver a utilizar',
                        choices=['firefox','chrome'],
                        default='firefox')
    parser.add_argument('--pool',
                        dest = 'pool',
                        help='indicar los numeros de hilos a utilizar',
                        type = int,
                        default=8)
    args = parser.parse_args()
    main()

