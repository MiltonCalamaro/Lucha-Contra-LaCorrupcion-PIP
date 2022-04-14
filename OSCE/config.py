import os
from os.path import join

PATH_OUTPUT = 'results'
os.makedirs(PATH_OUTPUT, exist_ok=True)

URL_ADJUDICACION = 'https://tinyurl.com/conosceadjudicacionecd{annio}'
PATH_ADJUDICACION = join(PATH_OUTPUT, 'adjudicacion')
os.makedirs(PATH_ADJUDICACION, exist_ok=True)

URL_CONTRATO = 'https://tinyurl.com/conoscecontratos{annio}'
PATH_CONTRATO = join(PATH_OUTPUT, 'contrato')
os.makedirs(PATH_CONTRATO, exist_ok=True)

URL_CONVOCATORIA = 'https://tinyurl.com/conosceconvocatoriascd{annio}'
PATH_CONVOCATORIA = join(PATH_OUTPUT, 'convocatoria')
os.makedirs(PATH_CONVOCATORIA, exist_ok=True)

URL_PROVEEDOR = 'https://tinyurl.com/conosceproveedores{annio}'
PATH_PROVEEDOR = join(PATH_OUTPUT, 'proveedor')
os.makedirs(PATH_PROVEEDOR, exist_ok=True)

URL_CONSORCIO = 'https://tinyurl.com/conosceconsorcios{annio}'
PATH_CONSORCIO = join(PATH_OUTPUT, 'consorcio')
os.makedirs(PATH_CONSORCIO, exist_ok=True)

URL_POSTOR = 'https://tinyurl.com/CONOSCEPOSTORES{annio}'
PATH_POSTOR = join(PATH_OUTPUT, 'postor')
os.makedirs(PATH_POSTOR, exist_ok=True)

URL_COMITE_SELECCION = 'https://tinyurl.com/conoscecomite{annio}'
PATH_COMITE_SELECCION = join(PATH_OUTPUT, 'comite_seleccion')
os.makedirs(PATH_COMITE_SELECCION, exist_ok=True)

URL_CONFORMACION_JURIDICA = 'https://tinyurl.com/conosceconformacion'
PATH_CONFORMACION_JURIDICA = join(PATH_OUTPUT, 'conformacion_juridica')
os.makedirs(PATH_CONFORMACION_JURIDICA, exist_ok=True)

URL_ENTIDAD_CONTRATANTE = 'https://tinyurl.com/CONOSCEENTIDADCONTRATANTE'
PATH_ENTIDAD_CONTRATANTE = join(PATH_OUTPUT, 'entidad_contratante')
os.makedirs(PATH_ENTIDAD_CONTRATANTE, exist_ok=True)

# https://tinyurl.com/CONOSCEPENALIDADES
# https://tinyurl.com/CONOSCEPENALIDADES20182020

# https://tinyurl.com/CONOSCESANCIONADOS
# https://tinyurl.com/CONOSCESANCIONADOSMULTA

# https://tinyurl.com/CONOSCEINHABILITAJUDICIAL

# PLAN_ANUAL_CONTRATACIONES = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertospac.html/content?userid=public&password=key'
# DATOS_CONVOCATORIAS = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertosconvocatorias.html/content?userid=public&password=key'
# DATOS_ADJUDICACION = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertosadjudicaciones.html/content?userid=public&password=key'
# LISTADO_OFERTANTES = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertospostor.html/content?userid=public&password=key'
# PROVEEDORES_Y_CONSORCIOS = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertosproveedores.html/content?userid=public&password=key'
# CONTRATOS = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertoscontratos.html/content?userid=public&password=key'
# MIEMBROS_COMITE = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertoscomite.html/content?userid=public&password=key'
# DATOS_PRONUNCIAMIENTOS = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertospronunciamientos.html/content?userid=public&password=key'
# CONFORMACION_JURIDICA_PROVEEDORES = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertoscomposicion.html/content?userid=public&password=key'
# SANCIONES_PROVEEDORES = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertospenalidades.html/content?userid=public&password=key'
# ENTIDADES_CONTRATANTES = 'https://bi.seace.gob.pe/pentaho/api/repos/%3Apublic%3Aportal%3Adatosabiertosentidadescontratantes.html/content?userid=public&password=key'