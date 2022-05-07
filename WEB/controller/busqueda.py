import pandas as pd
import mysql.connector as mysql

def buscador_basico(CodPip, CodSnip, NomCta, CodCto, NomCte, MonTotCtoMin, MonTotCtoMax, FecIniCto, FecFinCto, NomSec, CodConv, NumeroResultado):
    con = mysql.connect(host = 'db-dsrp-dev.cdykihpovon2.us-east-1.rds.amazonaws.com',
                        port = '3306',
                        user = 'admin',
                        database = 'dsrp',
                        password = 't8P2uEeRHsiDnCEDaaRE'
                    )

    NumeroResultado = int(NumeroResultado/2)

    query_proyectos = """
    select 
    'proyecto' as TipoTarjeta,
    tp.CodPip as CodigoUnico,
    tp.NomPip as NombreProyecto,
    cte.NomCte as NombreContratante,
    tu.DepUbi as Departamento,
    tu.ProUbi as Provincia,
    tu.DistUbi as Distrito,
    tf.DesFun as Funcion,
    tp.EtaPip as Etapa,
    tp.EstPip as Estado
    from dsrp.tabla_pip tp 
    left join dsrp.tabla_contratante cte on cte.CodCte = tp.CodCte 
    left join dsrp.tabla_ubigeo tu on tu.CodUbi = tp.CodUbi 
    left join dsrp.tabla_funcion tf on tf.CodFun = tp.CodFun 
    where 1=1
    """
    if (CodPip == '' and CodSnip == '' and NomCte == '' and NumeroResultado == ''):
        query_proyectos += f" and tp.CodPip = 'null'"
    if CodPip:
        query_proyectos += f" and tp.CodPip = '{CodPip}'"
    if CodSnip:
        query_proyectos += f" and tp.CodSniPip = '{CodSnip}'"
    if NomCte:
        query_proyectos += f" and cte.NomCte like '%{NomCte}%'"

    query_proyectos += f' limit {NumeroResultado}'

    print(query_proyectos)
    df_proyectos = pd.read_sql(query_proyectos, con)

    print(df_proyectos.head())

    query_contratos = """
    select 
    'contrato' as TipoTarjeta,
    tc.CodCto as CodigoContrato,
    cte.NomCte as EntidadPublica,
    cta.NomCta as Proveedor,
    tc.FecIniCto as FechaInicio,
    tc.FecFinCto as FechaFin,
    tc.MonTotCto as MontoContrato,
    ts.NomSec as NombreSector,
    tc.NroCodCto as NumeroContrato,
    tc.FecSusCto as FechaSuscripcion
    from dsrp.tabla_adjudicacion ta 
    inner join dsrp.tabla_contratante cte on cte.CodCte = ta.CodCte 
    inner join dsrp.tabla_contratista cta on cta.CodCta = ta.CodCta
    inner join dsrp.tabla_contrato tc on tc.CodAdj = ta.CodAdj 
    inner join dsrp.tabla_convocatoria tc2 on tc2.CodConv = ta.CodConv 
    inner join dsrp.tabla_sector ts on ts.CodSec = tc2.CodSec 
    where 1=1
    """
    if (CodCto == '' and NomCte == '' and  MonTotCtoMin == '' and MonTotCtoMax == '' and FecIniCto == '' and FecFinCto == '' and NomCta == '' and CodConv == '' and NomSec == '' and NumeroResultado ==''):
        query_contratos += f" and tc.CodCto like 'null'"
    if CodCto:
        query_contratos += f" and tc.CodCto like '%{CodCto}%'"
    if FecIniCto:
        query_contratos += f" and tc.FecIniCto >= {FecIniCto}"
    if FecFinCto:
        query_contratos += f" and tc.FecFinCto <= {FecFinCto}"
    if MonTotCtoMin:
        query_contratos += f" and tc.MonTotCto >= {MonTotCtoMin}"
    if MonTotCtoMax:
        query_contratos += f" and tc.MonTotCto <= {MonTotCtoMax}"
    if NomCte:
        query_contratos += f" and cte.NomCte like '%{NomCte}%'"
    if NomCta:
        query_contratos += f" and cta.NomCta like '%{NomCta}%'"
    if CodConv:
        query_contratos += f" and ta.CodConv = '{CodConv}'"
    if NomSec:
        query_contratos += f" and ts.NomSec like '%{NomSec}%'"

    query_contratos += f' limit {NumeroResultado}'

    df_contratos = pd.read_sql(query_contratos, con)
    
    print(df_contratos.head())

    if not (df_contratos.empty or df_proyectos.empty) :
        json_contratos = df_contratos.to_json(orient='records')
        json_proyectos = df_proyectos.to_json(orient='records')
        json_data = '{"CONTRATOS" :'+json_contratos +', "PROYECTOS" :'+ json_proyectos+'}'
        print('data contrato y data proyecto existen')
        print(json_data)
        return json_data
    if not df_contratos.empty:
        print('data contrato existen')
        json_contratos = df_contratos.to_json(orient='records')
        print(json_contratos)
        return '{"CONTRATOS" :'+json_contratos+'}'
    if not df_proyectos.empty:
        print('data proyecto existen')
        json_proyectos = df_proyectos.to_json(orient='records')
        print(json_proyectos)
        return '{"PROYECTOS" :'+json_proyectos+'}'
    else:
        return '[]'





