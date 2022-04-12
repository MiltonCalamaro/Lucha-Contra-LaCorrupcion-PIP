import os
URL_SSI = 'https://ofi5.mef.gob.pe/ssi/ssi/Index'
URL_MEF_API = 'https://datosabiertos.mef.gob.pe/api/3/action/datastore_search'
URL_MEF = 'https://datosabiertos.mef.gob.pe'
PATH_OUTPUT = 'results'
FILENAME_OUTPUT = 'ssi_data.json'
os.makedirs(PATH_OUTPUT, exist_ok=True)

fields = ['SECTOR','ENTIDAD','NIVEL',
          'CODIGO_UNICO','CODIGO_SNIP','NOMBRE_UEP',
          'FUNCION','PROGRAMA','SUBPROGRAMA','MARCO','DES_MODALIDAD',
          'FECHA_ULT_ACT_F12B','ULT_FEC_DECLA_ESTIM','TIENE_F12B',
          'PROG_ACTUAL_AÑO_ACTUAL','MONTO_VALORIZACION',
          'DEV_AÑO_ACTUAL','TIENE_AVAN_FISICO',
          'SANEAMIENTO','ETAPA_F8',
          'AVANCE_FISICO','AVANCE_EJECUCION',
          'DEPARTAMENTO','PROVINCIA','DISTRITO','UBIGEO','LATITUD','LONGITUD']

params = {'resource_id': '7d2995ab-826f-4da6-aafd-30e8e4f6a657',
          'limit': '1000',
          'fields': ",".join(fields)}

# QUERY_PROYECTO = {
# 'CUSCO':'{%22TIPO_INVERSION%22:%22PROYECTO%20DE%20INVERSION%22,%22DEPARTAMENTO%22:%22CUSCO%22}'}
QUERY_PROYECTO ="%7B%22TIPO_INVERSION%22%3A%22PROYECTO+DE+INVERSION%22%2C%22DEPARTAMENTO%22%3A%22{region}%22%7D"

REGION_LIST  = ['-MUL.DEP-','AMAZONAS','ANCASH','APURIMAC','AREQUIPA','AYACUCHO','CAJAMARCA','CALLAO','CUSCO',
                'HUANCAVELICA','HUANUCO','ICA','JUNIN','LA LIBERTAD','LAMBAYEQUE','LIMA','LORETO','MADRE DE DIOS',
                'MOQUEGUA','PASCO','PIURA','PUNO','SAN MARTIN','TACNA','TUMBES','UCAYALI']
