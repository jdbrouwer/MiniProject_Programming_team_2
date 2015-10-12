import urllib.request
import hjson
import codecs

url = 'http://www.filmtotaal.nl/api/filmsoptv.xml?apikey=zmp3tnvbezlo4gbl4bh0mkro5e63xzkb&dag=12-10-2015&sorteer=2'
req = urllib.request.urlopen(url)
data = hjson.load(req)

def schrijf_xml(data):
    bestand = open('filmlijst.xml', 'w')
    bestand = codecs.open('filmlijst.xml', "w", "utf-8")
    bestand.write(str(data))
    bestand.close()
schrijf_xml(data)