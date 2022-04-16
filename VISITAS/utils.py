import json
from config import PATH_OUTPUT, FILENAME_OUTPUT, EXECUTABLE_PATH_GECKODRIVER, EXECUTABLE_PATH_CHROMEDRIVER
from selenium import webdriver
import logging
import yaml

__config = None
def config():
	global __config
	if not __config:
		with open('query.yaml', mode="r", encoding='utf-8') as f:
			__config=yaml.full_load(f)
	return __config

def config_option(option):
    option.add_argument('--no-sandbox') 
    option.add_argument('--disable-dev-shm-usage')
    return option

def create_driver(driver):
    if driver=='firefox':
        option = webdriver.FirefoxOptions()
        option = config_option(option)
        option.add_argument("--headless")
        browser = webdriver.Firefox(options=option,  executable_path=EXECUTABLE_PATH_GECKODRIVER)
    if driver=='chrome':
        option = webdriver.ChromeOptions()
        option = config_option(option)
        browser = webdriver.Chrome(options=option, executable_path=EXECUTABLE_PATH_CHROMEDRIVER)
    return browser

def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s, %(levelname)s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
        logging.StreamHandler()
        ]
    )
    logger = logging.getLogger(f":__{name}__:")
    return logger

def save_json(data, filename=FILENAME_OUTPUT):
    with open(f"{PATH_OUTPUT}/{filename}", mode='w', encoding='utf-8') as f:
        json.dump(data, f)