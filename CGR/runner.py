import unittest
import sys
import argparse
from utils import create_driver, save_json
from extraction import SeleniumCGR

class TestCGR(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = create_driver(args.driver)
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()

    def tearDown(self) -> None:
        self.driver.close()
    
    def test_cgr(self):
        browser = self.driver
        selenium_cgr = SeleniumCGR(browser)
        data = selenium_cgr.data
        save_json(data)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--driver',
                        dest = 'driver',
                        help = 'indicar el driver a utilizar',
                        choices=['firefox','chrome'])

    ns, args = parser.parse_known_args(namespace=unittest)
    return ns, sys.argv[:1] + args

if __name__=='__main__':
    args, argv = parse_args()  
    sys.argv[:] = argv 
    unittest.main()
