import os
### urls 
URL_RUC = 'https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias'
URL_RUC_API = 'https://ruc.com.pe/api/v1/consultas'

### path_output
PATH_OUTPUT = 'results'
os.makedirs(PATH_OUTPUT, exist_ok=True)

### encabezado y cuerpo api
headers = {'Content-Type': 'application/json'}
params = {
  "token": "25a017dc-83d9-46b7-b995-f362d0f139c8-329eb914-f8bf-4b0d-9cae-9eb173e9b204",
  "ruc": ""
}

### para interactuar con la pagina
xpath_input = "//*[@id='txtRuc']"
xpath_buscar = "//*[@id='btnAceptar']"
xpath_regresar = '/html/body/div/div[2]/div/div[2]/button'

### para extraer los valores
# https://www.seleniumeasy.com/selenium-tutorials/xpath-tutorial-for-selenium
xpath_nroRuc = "//*[contains(text(), 'Número de RUC')]/parent::*/following-sibling::*"
xpath_tipoContr = "//*[contains(text(), 'Tipo Contribuyente')]/parent::*/following-sibling::*"
xpath_nombrCome = "//*[contains(text(), 'Nombre Comercial')]/parent::*/following-sibling::*"
xpath_fechaIns = "//*[contains(text(), 'Fecha de Inscripción')]/parent::*/following-sibling::div[1]/p"
xpath_fechaIni = "//*[contains(text(), 'Fecha de Inicio de Actividades')]/parent::*/following-sibling::div[1]/p"
xpath_estContr = "//*[contains(text(), 'Estado del Contribuyente')]/parent::*/following-sibling::*"
xpath_condContr = "//*[contains(text(), 'Condición del Contribuyente')]/parent::*/following-sibling::*"
xpath_domiFisc = "//*[contains(text(), 'Domicilio Fiscal')]/parent::*/following-sibling::*"
xpath_sistEmis = "//*[contains(text(), 'Sistema Emisión de Comprobante')]/parent::*/following-sibling::div[1]"
xpath_actiComex = "//*[contains(text(), 'Actividad Comercio Exterior')]/parent::*/following-sibling::div[1]"
xpath_sistConta = "//*[contains(text(), 'Sistema Contabilidiad')]/parent::*/following-sibling::*"
xpath_actiEcono = "//*[contains(text(), 'Actividad(es) Económica(s)')]/parent::*/following-sibling::*" ## //tr plural
xpath_sistElect = "//*[contains(text(), 'Sistema de Emisión Electrónica')]/parent::*/following-sibling::*" ##//tr plural
xpath_emisorElect = "//*[contains(text(), 'Emisor electrónico desde')]/parent::*/following-sibling::*"
xpath_comproElect = "//*[contains(text(), 'Comprobantes Electrónicos')]/parent::*/following-sibling::*"
xpath_afiliDesde = "//*[contains(text(), 'Afiliado al PLE desde')]/parent::*/following-sibling::*"
xpath_padrones = "//*[contains(text(), 'Padrones')]/parent::*/following-sibling::*"

dict_features  = {'nro_ruc':xpath_nroRuc, 'tipo_contribuyente':xpath_tipoContr, 
                'nombre_comercial':xpath_nombrCome,'fecha_inscripcion':xpath_fechaIns,
                'fecha_inicio':xpath_fechaIni,'estado_contribuyente':xpath_estContr,
                'condicion_contribuyente':xpath_condContr, 'sistema_comprobante':xpath_sistEmis,
                'actividad_comex':xpath_actiComex, 'sistema_contabilidad':xpath_sistConta, 
                'actividad_economica':xpath_actiEcono, 'sistema_electronico':xpath_sistElect,
                'emisor_electronico_desde':xpath_emisorElect, 
                'comprobante_electronico':xpath_comproElect,
                'afiliado_ple_desde':xpath_afiliDesde, 'padron':xpath_padrones}