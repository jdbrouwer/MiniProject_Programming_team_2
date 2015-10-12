import codecs
import requests
import datetime
def datum():
    i = datetime.datetime.now()
    date = ("%s-%s-%s" % (i.day, i.month, i.year) )
    print(date)
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

apicall()



