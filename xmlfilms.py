import codecs
import requests
import datetime
import xmltodict

def datum(): 
    i = datetime.datetime.now()
    date = ("%s-%s-%s" % (i.day, i.month, i.year) )
    return date


def schrijf_xml(data):
    bestand = open('filmlijst.xml', 'w')
    bestand = codecs.open('filmlijst.xml', "w", "utf-8")
    bestand.write(str(data))
    bestand.close()


def apicall():
    date = datum()
    response = requests.get('http://www.filmtotaal.nl/api/filmsoptv.xml?apikey=zmp3tnvbezlo4gbl4bh0mkro5e63xzkb&dag='+date+'&sorteer=0')
    response.encoding='utf-8'
    schrijf_xml(response.text)

def read_xml():
    bestand = open('filmlijst.xml', 'r')
    xml_string= bestand.read()
    return xmltodict.parse(xml_string)

def list_titels(lijst):
    list = []
    for film in lijst['filmsoptv']['film']:
        list.append(film['titel'])
    return(list)

def list_begin_time(lijst):
    list = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['starttijd'])
        ).strftime('%Y-%m-%d %H:%M:%S')
        list.append(bewerk)
    print(list)
    return(list)

def list_eind_time(lijst):
    list = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['eindtijd'])
        ).strftime('%Y-%m-%d %H:%M:%S')
        list.append(bewerk)
    print(list)
    return(list)

data_xml = read_xml()
titel_lijst = list_titels(data_xml)
begin_tijd = list_begin_time(data_xml)
eind_tijd = list_eind_time(data_xml)


apicall()