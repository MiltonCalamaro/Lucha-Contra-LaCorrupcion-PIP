import subprocess
import logging
### TRANSPARENCIA OK
### Utilizando driver firefox
subprocess.run(['python','runner.py', '--poder', 'presidencia', '--since', '2012-01-01'], cwd = 'VISITAS')
### Utilizando beautilfulSoup
subprocess.run(['python','runner.py', '--poder', 'presidencia', '--last'], cwd = 'VISITAS')
### Utilizando API
subprocess.run(['python','runner.py', '--poder', 'congreso', '--since', '2020-01-01'], cwd = 'VISITAS')
### Utilizando API
subprocess.run(['python','runner.py', '--poder', 'congreso', '--last'], cwd = 'VISITAS')

## CGR OK
## Utilizando driver firefox
subprocess.run(['python','runner.py','--since','2017-01-01'], cwd = 'CGR')
## Utilizando driver firefox
subprocess.run(['python','runner.py','--last'], cwd = 'CGR')

### OSCE OK
## Descargando archivos de la pagina OSCE
subprocess.run(['python','extraction.py','--annios',"2018 2019 2020 2021 2022"], cwd = 'OSCE')

### MEF, diseñar la extracion de los ultimos proyectos
### Utilizando driver firefox
for region in ['CUSCO','LAMBAYEQUE','LORETO','LIMA','PIURA']:
    subprocess.run(['python', 'runner.py', '--region', region], cwd = 'MEF')
    subprocess.run(['python', 'runner.py', '--region', region, '--last' ], cwd = 'MEF')
### SUNAT
#  python .\runner.py --ruc .\test.json -m scraper
