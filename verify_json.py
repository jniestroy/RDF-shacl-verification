import requests
from pyshacl import validate

def validate_meta(func):
    def authenticate_and_call(testjson):
        if not validate_json(testjson): 
            raise Exception('Validation Failed.')
        return func(testjson)
    return authenticate_and_call

@validate_meta
def hi(testjson):
    print("Hi")


def validate_json(testjson):
    shapes_file = '''
    @prefix dash: <http://datashapes.org/dash#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix schema: <http://schema.org/> .
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    schema:DatasetShape
        a sh:NodeShape ;
        sh:targetClass schema:Dataset ;
        sh:property [
            sh:path schema:name ;
            sh:datatype xsd:string ;
            sh:name "dataset name" ;
        ] ;
        sh:property [
            sh:path schema:description ;
            sh:datatype xsd:string ;
            sh:name "dataset description" ;
        ] ;
        sh:property [
            sh:path schema:author ;
        ] ;
        sh:property [
            sh:path schema:gender ;
            sh:in ( "female" "male" ) ;
        ] ;
        sh:property [
            sh:path schema:dateCreated ;
            sh:maxCount 1 ;
        ] .
    '''
    shapes_file_format = 'turtle'
    data_file_format = 'json-ld'

    conforms, v_graph, v_text = validate(data_file, shacl_graph=shapes_file,
                                     data_graph_format=data_file_format,
                                     shacl_graph_format=shapes_file_format,
                                     inference='rdfs', debug=True,
                                     serialize_report_graph=True)
    return(conforms)
  

data_file = '''
{
  "@context":{ "@vocab": "http://schema.org/" },
  "@type":"Dataset",
  "dateCreated":"19/9/1995",
  "dateCreated":10,
  "name":5,
  "description":"Storm Data is provided by the National Weather Service (NWS) and contain statistics on...",
  "url":"https://catalog.data.gov/dataset/ncdc-storm-events-database",
  "sameAs":"https://gis.ncdc.noaa.gov/geoportal/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510",
  "identifier": ["https://doi.org/10.1000/182",
                 "https://identifiers.org/ark:/12345/fk1234"],
  "keywords":[
     "ATMOSPHERE > ATMOSPHERIC PHENOMENA > CYCLONES",
     "ATMOSPHERE > ATMOSPHERIC PHENOMENA > DROUGHT",
     "ATMOSPHERE > ATMOSPHERIC PHENOMENA > FOG",
     "ATMOSPHERE > ATMOSPHERIC PHENOMENA > FREEZE"
  ],
  "author":{
     "@type":"Organization",
     "url": "https://www.ncei.noaa.gov/",
     "name":"OC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce",
     "contactPoint":{
        "@type":"ContactPoint",
        "contactType": "customer service",
        "telephone":"+1-828-271-4800",
        "email":"ncei.orders@noaa.gov"
     }
  },
  "includedInDataCatalog":{
     "@type":"DataCatalog",
     "name":"data.gov"
  },
  "distribution":[
     {
        "@type":"DataDownload",
        "encodingFormat":"CSV",
        "contentUrl":"http://www.ncdc.noaa.gov/stormevents/ftp.jsp"
     },
     {
        "@type":"DataDownload",
        "encodingFormat":"XML",
        "contentUrl":"http://gis.ncdc.noaa.gov/all-records/catalog/search/resource/details.page?id=gov.noaa.ncdc:C00510"
     }
  ]
}
'''
try:
    hi(data_file)
except:
    print('Made it past')

