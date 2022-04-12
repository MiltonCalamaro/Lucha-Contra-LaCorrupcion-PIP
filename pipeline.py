#  python .\runner.py --ruc .\test.json -m scraper
import subprocess
from multiprocessing.dummy import Pool
pool = Pool(25)

list_test = range(5)
def run(test):
    subprocess.run(['python', 'runner.py', '--ruc', 'test.json', '--method', 'scraper'], cwd='RUC/')
pool.map(run, list_test)