import unittest
import argparse
import sys
import json
from extraction import SeleniumRuc, RucApi
from utils import create_driver, save_json
from multiprocessing.dummy import Pool
pool = Pool(25)

#  python .\runner.py --ruc .\test.json -m api
#  python .\runner.py --ruc .\test.json -m scraper

class TestPley(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = create_driver()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()

    def test_selenium_ruc(self):
        browser = self.driver
        selenium_ruc = SeleniumRuc(browser, list_ruc)
        save_json(selenium_ruc.data)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ruc','-r',
                        dest = 'ruc',
                        help = 'indicar la lista de ruc a extraer')

    parser.add_argument('--method', '-m',
                        dest = 'method',
                        choices=['scraper','api'])

    ns, args = parser.parse_known_args(namespace=unittest)
    return ns, sys.argv[:1] + args

def get_api_ruc(list_ruc):
    list_data = []
    for ruc_api in pool.map(RucApi, list_ruc):
        if ruc_api.data:
            list_data.append(ruc_api.data)
    save_json(list_data)

if __name__ == '__main__':
    args, argv = parse_args()  
    sys.argv[:] = argv 

    with open(args.ruc, mode='r', encoding='utf-8') as f:
        list_ruc = json.load(f)
        
    if args.method=='scraper':
        unittest.main()

    if args.method=='api':
        get_api_ruc(list_ruc)
