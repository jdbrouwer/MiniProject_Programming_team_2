import urllib.request
import hjson
import codecs
import xmltodict

url = 'http://www.filmtotaal.nl/api/filmsoptv.xml?apikey=zmp3tnvbezlo4gbl4bh0mkro5e63xzkb&dag=12-10-2015&sorteer=2'
req = urllib.request.urlopen(url)
data = hjson.load(req)

def schrijf_xml(data):
    bestand = open('filmlijst.xml', 'w')
    bestand = codecs.open('filmlijst.xml', 'w', 'utf-8')
    bestand.write(str(data))
    bestand.close()

def lees_xml():
    bestand = open('filmlijst.xml', 'r')
    xml_string = bestand.read()
    return xmltodict.parse(xml_string)

def film_name(filmbestand):
    list = []
    for film in filmbestand['film']['titel']:
        list.append(film['titel'])
    print(list)
    return list

filmbestand = lees_xml()
film_name(filmbestand)


schrijf_xml(data)