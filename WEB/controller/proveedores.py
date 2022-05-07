import mysql.connector as mysql
import pandas as pd


def querys(RucContratista):
    
    #RucContratista = '20100011884'
    
    con = mysql.connect(host = 'db-dsrp-dev.cdykihpovon2.us-east-1.rds.amazonaws.com',
                        port = '3306',
                        user = 'admin',
                        database = 'dsrp',
                        password = 't8P2uEeRHsiDnCEDaaRE'
                    )

    queryContratacionesRapidas = open('querys/contrataciónRapida.txt')
    queryContratacionesRapidas = queryContratacionesRapidas.read()
    queryContratacionesRapidas = queryContratacionesRapidas.replace('$$$RucContratista', RucContratista)

    queryContratistasVisitantes = open('querys/contratistasVisitantes.txt')
    queryContratistasVisitantes = queryContratistasVisitantes.read()
    queryContratistasVisitantes = queryContratistasVisitantes.replace('$$$RucContratista', RucContratista)

    queryContratoPositivos = open('querys/montoContratoPositivo.txt')
    queryContratoPositivos = queryContratoPositivos.read()
    queryContratoPositivos = queryContratoPositivos.replace('$$$RucContratista', RucContratista)

    queryContratoNegativos = open('querys/montoContratosNegativo.txt')
    queryContratoNegativos = queryContratoNegativos.read()
    queryContratoNegativos = queryContratoNegativos.replace('$$$RucContratista', RucContratista)

    queryRedContratistas = open('querys/redContratistas.txt')
    queryRedContratistas = queryRedContratistas.read()
    queryRedContratistas = queryRedContratistas.replace('$$$RucContratista', RucContratista)
    
    querySancionesPenalidades = open('querys/sancionesPenalidades.txt')
    querySancionesPenalidades = querySancionesPenalidades.read()
    querySancionesPenalidades = querySancionesPenalidades.replace('$$$RucContratista', RucContratista)

    dfContratacionesRapidas = pd.read_sql(queryContratacionesRapidas, con)
    
    dfContratistasVisitantes = pd.read_sql(queryContratistasVisitantes, con)
    
    dfContratosPositivos =  pd.read_sql(queryContratoPositivos, con)

    dfContratosNegativos =  pd.read_sql(queryContratoNegativos, con)

    dfRedContratistas = pd.read_sql(queryRedContratistas, con)    
    
    dfSancionesPenalidades = pd.read_sql(querySancionesPenalidades, con)    
 
    if dfSancionesPenalidades.empty and dfRedContratistas.empty and dfContratosNegativos.empty and dfContratistasVisitantes.empty and dfContratacionesRapidas.empty :
        res = '[]'
        return res

    data =  {
        "ContratacionesRapidas" : str(dfContratacionesRapidas['AvgFecDiff'][0]),
        "ContratistasVisitantes" : str(len(dfContratistasVisitantes)),
        "MontoContratos" : {
            "DiferenciasPositivos": str(dfContratosPositivos['MontDiffPorc'][0]),
            "DiferenciasNegativos": str(dfContratosNegativos['MontDiffPorc'][0]) 
            },
        "RedContratistas" : str(len(dfRedContratistas)),
        "Sanciones" : str(dfSancionesPenalidades['n_sancionTCE'][0]),
        "Penalidades" : str(dfSancionesPenalidades['n_penalidad'][0])

        }
    
    return data









