import os
EXECUTABLE_PATH_GECKODRIVER='/usr/local/bin/geckodriver'
EXECUTABLE_PATH_CHROMEDRIVER='D://chromedriver.exe'

### urls 
URL_RUC = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias'
URL_RUC_API = 'https://ruc.com.pe/api/v1/consultas'

### path output
PATH_OUTPUT = 'results'
os.makedirs(PATH_OUTPUT, exist_ok=True)
### filename output
FILENAME_OUTPUT = 'ruc_data.json'

### encabezado y cuerpo api
headers = {'Content-Type': 'application/json'}
params = {
  "token": "25a017dc-83d9-46b7-b995-f362d0f139c8-329eb914-f8bf-4b0d-9cae-9eb173e9b204",
  "ruc": ""
}
