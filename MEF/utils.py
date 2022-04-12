import json
import logging
from config import PATH_OUTPUT, FILENAME_OUTPUT
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import yaml
__config = None
def config():
	global __config
	if not __config:
		with open('query.yaml', mode="r", encoding='utf-8') as f:
			__config=yaml.full_load(f)
	return __config

def create_driver():
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--host-resolver-rules=MAP www.google-analytics.com 127.0.0.1")
    option.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36')
    s = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=s, options=option)
    return browser

def save_json(data, filename=FILENAME_OUTPUT):
    with open(f"{PATH_OUTPUT}/{filename}", mode='w', encoding='utf-8') as f:
        json.dump(data, f)

def get_logger(name):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s, %(levelname)s %(name)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
        # logging.FileHandler(f"../log/{name}_{time.strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
        ]
)
    logger = logging.getLogger(f":__{name}__:")
    return logger