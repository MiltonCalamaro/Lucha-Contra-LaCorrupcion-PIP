import subprocess
### MEF, diseñar la extracion de los ultimos proyectos
subprocess.run(['python','runner.py','--region','CUSCO','--driver','firefox','--pool','16'], cwd = 'MEF')
subprocess.run(['python','runner.py','--region','LAMBAYEQUE','--driver','firefox','--pool','16'], cwd = 'MEF')
subprocess.run(['python','runner.py','--region','LORETO','--driver','firefox','--pool','16'], cwd = 'MEF')
subprocess.run(['python','runner.py','--region','LIMA','--driver','firefox','--pool','16'], cwd = 'MEF')
subprocess.run(['python','runner.py','--region','PIURA','--driver','firefox','--pool','16'], cwd = 'MEF')
### CGR, diseñar las extraction de los ultimos y configurado por fechas
subprocess.run(['python','runner.py','--driver','firefox'], cwd = 'CGR')
### OSCE
subprocess.run(['python','extraction.py','--annios',"2018 2019 2020 2021 2022"], cwd = 'OSCE')
### TRANSPARENCIA, falta lo de congresistas
subprocess.run(['python','runner.py','--driver','firefox','--since','2017-01-01','--pool','16'], cwd = 'VISITAS')
### RUC
#  python .\runner.py --ruc .\test.json -m scraper
