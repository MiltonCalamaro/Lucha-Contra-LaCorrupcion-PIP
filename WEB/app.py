from flask import Flask, json, request
from flask_cors import CORS, cross_origin
from controller import busqueda, sector, proveedores


app = Flask(__name__)

CORS(app)

@cross_origin
@app.route("/")
def hello_world():
    return "UREP TECH API"

@cross_origin
@app.route("/buscador-basico",methods=['POST'])
def buscador():
    print(request.json) 
    req = request.json
    CodPip = req['CodigoProyectoInversionPublica']
    CodSnip = req['CodigoSNIP']
    CodConv = req['CodigoConvocatoria']
    NomCta = req['NombreContratista']
    NomCte = req['NombreContratante']
    CodCto = req['CodigoContrato']
    MonTotCtoMin = req['MontoTotalContratoMinimo']
    MonTotCtoMax = req['MontoTotalContratoMaximo']
    FecIniCto = req['FechaInicioContrato']
    FecFinCto = req['FechaFinContrato']
    NomSec = req['NombreSector']
    NumeroResultado =  int(req['NumeroResultado'])
    res = busqueda.buscador_basico(CodPip, CodSnip, NomCta, CodCto, NomCte, MonTotCtoMin, MonTotCtoMax, FecIniCto, FecFinCto, NomSec, CodConv, NumeroResultado)
    # res = data.to_json(orient='records', force_ascii=False)
    #return json.dumps(res),200,{'Content-Type': 'application/json; charset=utf-8'}
    print(type(res))
    return json.dumps(res),200,{'Content-Type': 'application/json; charset=utf-8'}


@cross_origin
@app.route("/sector")
def sector_funcion():
    res = sector.query()
    return res


@cross_origin
@app.route('/buscador_proveedores', methods = ['POST'])
def buscadorProveedores():
    req = request.json
    RucContratista = str(req['RucContratista'])
    print(RucContratista)
    print(len(RucContratista))
    if not (len(RucContratista) == 11):
        res = '[]'
        return json.dumps(res),200,{'Content-Type': 'application/json; charset=utf-8'}
    if ( (RucContratista.startswith('2') == False) and (RucContratista.startswith('1') == False)):
        res = '[]'
        return json.dumps(res),200,{'Content-Type': 'application/json; charset=utf-8'}
    res = proveedores.querys(RucContratista)
    return json.dumps(res),200,{'Content-Type': 'application/json; charset=utf-8'}







