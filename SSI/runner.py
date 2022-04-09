import unittest
import argparse
import sys
import json
from utils import create_driver, save_json
from extraction import SeleniumSSI
import warnings as w
w.filterwarnings('ignore')

class TestSeleniumRUC(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = create_driver()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()

    def test_selenium_ruc(self):
        browser = self.driver
        selenium_ssi = SeleniumSSI(browser, list_ruc)
        save_json(selenium_ssi.data)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cui',
                        dest = 'cui',
                        help = 'indicar la lista de cui a extraer')

    ns, args = parser.parse_known_args(namespace=unittest)
    return ns, sys.argv[:1] + args

if __name__ == '__main__':
    args, argv = parse_args()  
    sys.argv[:] = argv 


    with open(args.cui, mode='r', encoding='utf-8') as f:
        list_ruc = json.load(f)
        
    unittest.main()