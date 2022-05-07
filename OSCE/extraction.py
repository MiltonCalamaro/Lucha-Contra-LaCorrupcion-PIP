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
                    URL_ENTIDAD_CONTRATANTE, PATH_ENTIDAD_CONTRATANTE,
                    URL_PENALIDAD, URL_PENALIDAD_2018_2022, URL_SANCIONADO, URL_SANCIONADO_MULTA, URL_INHABILITACION, PATH_INFRACION_PROVEEDOR
                    )
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('__osce__')

def download_excel(url, filename):
    resp = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(resp.content)

def config_download(url, path, annio, format='xlsx'):
    url = url.format(annio=annio)
    filename = join(path, f"{basename(path)}_{annio}.{format}")
    download_excel(url, filename)

def main():
    list_annio = args.annios.split()
    for annio in list_annio:
        ### adjudicacion
        config_download(URL_ADJUDICACION, PATH_ADJUDICACION, annio)
        logger.info(f'download adjudicacion {annio}')
        ### contrato
        config_download(URL_CONTRATO, PATH_CONTRATO, annio)
        logger.info(f'download contrato {annio}')
        ### convocatoria
        config_download(URL_CONVOCATORIA, PATH_CONVOCATORIA, annio)      
        logger.info(f'download convocatoria {annio}')
        ### proveedor
        config_download(URL_PROVEEDOR, PATH_PROVEEDOR, annio)          
        logger.info(f'download proveedor {annio}')   
        ### consorcio
        config_download(URL_CONSORCIO, PATH_CONSORCIO, annio)             
        logger.info(f'download consorcio {annio}')
        ### postor
        config_download(URL_POSTOR, PATH_POSTOR, annio)                
        logger.info(f'download postor {annio}')
        ### comite seleccion
        config_download(URL_COMITE_SELECCION, PATH_COMITE_SELECCION, annio)                   
        logger.info(f'download comite seleccion {annio}')

    config_download(URL_CONFORMACION_JURIDICA, PATH_CONFORMACION_JURIDICA, '', format='csv')                   
    logger.info(f'download conformacion juridica')

    config_download(URL_ENTIDAD_CONTRATANTE, PATH_ENTIDAD_CONTRATANTE, '')                   
    logger.info(f'download entidad contratante')

    for url in [URL_PENALIDAD, URL_PENALIDAD_2018_2022, URL_SANCIONADO, URL_SANCIONADO_MULTA, URL_INHABILITACION]:
        config_download(url, PATH_INFRACION_PROVEEDOR,'')
        logger.info(f"download {basename(url)}")


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--annios',
                        dest='annios',
                        help='indicar la lista de años a extraer',
                        default='')
    args = parser.parse_args()
    main()

