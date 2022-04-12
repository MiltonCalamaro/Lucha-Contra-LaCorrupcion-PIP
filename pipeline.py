#  python .\runner.py --ruc .\test.json -m scraper
#  python .\runner.py --region "CALLAO" --driver chrome --pool 16
import subprocess
subprocess.run(['python','runner.py','--region','CUSCO','--driver','firefox','--pool','16'], cwd = 'MEF')
subprocess.run(['python','runner.py','--region','LAMBAYEQUE','--driver','firefox','--pool','16'], cwd = 'MEF')
subprocess.run(['python','runner.py','--region','LORETO','--driver','firefox','--pool','16'], cwd = 'MEF')
subprocess.run(['python','runner.py','--region','LIMA','--driver','firefox','--pool','16'], cwd = 'MEF')
subprocess.run(['python','runner.py','--region','PIURA','--driver','firefox','--pool','16'], cwd = 'MEF')
