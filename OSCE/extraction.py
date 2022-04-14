import requests
import argparse
from os.path import join, basename
from config import (URL_ADJUDICACION, PATH_ADJUDICACION, 
                    URL_CONTRATO, PATH_CONTRATO,
                    URL_CONVOCATORIA, PATH_CONVOCATORIA,
                    URL_PROVEEDOR, PATH_PROVEEDOR,
                    URL_CONSORCIO, PATH_CONSORCIO,
                    URL_POSTOR, PATH_POSTOR,
                    URL_COMITE_SELECCION, PATH_COMITE_SELECCION,
                    URL_CONFORMACION_JURIDICA, PATH_CONFORMACION_JURIDICA,
                    URL_ENTIDAD_CONTRATANTE, PATH_ENTIDAD_CONTRATANTE)
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('__osce__')

def download_excel(url, filename):
    resp = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(resp.content)

def config_download(url, path, annio):
    url = url.format(annio=annio)
    filename = join(path, f"{basename(path)}_{annio}.xlsx")
    download_excel(url, filename)

def main():
    list_annio = args.annios.split()
    for annio in list_annio:
        ### adjudicacion
        #url = URL_ADJUDICACION.format(annio=annio)
        #filename = f'{PATH_ADJUDICACION}/conosce_adjudicacion_{annio}.xlsx'
        #download_excel(annio, url, filename)
        config_download(URL_ADJUDICACION, PATH_ADJUDICACION, annio)
        logger.info(f'download adjudicacion {annio}')
        ### contrato
        # url = URL_CONTRATO.format(annio=annio)
        # filename = f'{PATH_CONTRATO}/conosce_contrato_{annio}.xlsx'
        # download_excel(annio, url, filename)
        config_download(URL_CONTRATO, PATH_CONTRATO, annio)
        logger.info(f'download contrato {annio}')
        ### convocatoria
        # url = URL_CONVOCATORIA.format(annio=annio)
        # filename = f'{PATH_CONVOCATORIA}/conosce_convocatoria_{annio}.xlsx'
        # download_excel(annio, url, filename)
        config_download(URL_CONVOCATORIA, PATH_CONVOCATORIA, annio)      
        logger.info(f'download convocatoria {annio}')
        ### proveedor
        # url = URL_PROVEEDOR.format(annio=annio)
        # filename = f'{PATH_PROVEEDOR}/conosce_proveedor_{annio}.xlsx'
        # download_excel(annio, url, filename)
        config_download(URL_PROVEEDOR, PATH_PROVEEDOR, annio)          
        logger.info(f'download proveedor {annio}')   
        ### consorcio
        # url = URL_CONSORCIO.format(annio=annio)
        # filename = f'{PATH_CONSORCIO}/conosce_consorcio_{annio}.xlsx'
        # download_excel(annio, url, filename)
        config_download(URL_CONSORCIO, PATH_CONSORCIO, annio)             
        logger.info(f'download consorcio {annio}')
        ### postor
        # url = URL_POSTOR.format(annio=annio)
        # filename = f'{PATH_POSTOR}/conosce_postor_{annio}.xlsx'
        # download_excel(annio, url, filename)
        config_download(URL_POSTOR, PATH_POSTOR, annio)                
        logger.info(f'download postor {annio}')
        ### comite seleccion
        # url = URL_COMITE_SELECCION.format(annio=annio)
        # filename = f'{PATH_COMITE_SELECCION}/conosce_comite_seleccion_{annio}.xlsx'
        # download_excel(annio, url, filename)
        config_download(URL_COMITE_SELECCION, PATH_COMITE_SELECCION, annio)                   
        logger.info(f'download comite seleccion {annio}')

    # url = URL_CONFORMACION_JURIDICA
    # filename = f'{PATH_CONFORMACION_JURIDICA}/conosce_conformacion_juridica.xlsx'
    # download_excel('', url, filename)   
    config_download(URL_CONFORMACION_JURIDICA, PATH_CONFORMACION_JURIDICA, '')                   
    logger.info(f'download conformacion juridica')

    # url = URL_ENTIDAD_CONTRATANTE
    # filename = f'{PATH_ENTIDAD_CONTRATANTE}/conosce_entidad_contratante.xlsx'
    # download_excel('', url, filename)
 
    config_download(URL_ENTIDAD_CONTRATANTE, PATH_ENTIDAD_CONTRATANTE, '')                   
    logger.info(f'download entidad contratante')


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--annios',
                        dest='annios',
                        help='indicar la lista de años a extraer')
    args = parser.parse_args()
    main()

