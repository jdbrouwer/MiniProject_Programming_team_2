#This is the main file of our python program:
import sqlite3
import codecs
import requests
import datetime
import xmltodict

#XML PART

def datum():
    #This function specifies the current date, this date is used in the request url
    i = datetime.datetime.now()
    date = ("%s-%s-%s" % (i.day, i.month, i.year) )
    return date


def schrijf_xml(data):
    #This function opens filmlijst.xml and writes it into a local xml file
    bestand = open('filmlijst.xml', 'w')
    bestand = codecs.open('filmlijst.xml', "w", "utf-8")
    bestand.write(str(data))
    bestand.close()


def apicall():
    #this function transfers data from the filmtotaal server, by using API, into the schrijf_xml function
    date = datum()
    response = requests.get('http://www.filmtotaal.nl/api/filmsoptv.xml?apikey=zmp3tnvbezlo4gbl4bh0mkro5e63xzkb&dag='+date+'&sorteer=0')
    response.encoding='utf-8'
    schrijf_xml(response.text)

def read_xml():
    #this function makes it so that the xml file can acctually be read like string
    bestand = open('filmlijst.xml', 'r')
    xml_string= bestand.read()
    return xmltodict.parse(xml_string)

#The functions below are used to create lists for titels, begin time and start time

def list_titels(lijst):
    #Here, the titles of the lists are added to a list
    list = []
    for film in lijst['filmsoptv']['film']:
        list.append(film['titel'])
    return(list)

def list_begin_time(lijst):
    #The begin times which are listed in the xml files will be put into a list
    list = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['starttijd'])
        ).strftime('%H:%M:%S')
        list.append(bewerk)
    return(list)

def list_end_time(lijst):
    #The end times which are listed in the xml files will be put into a list
    list = []
    for film in lijst['filmsoptv']['film']:
        bewerk = datetime.datetime.fromtimestamp(
            int(film['eindtijd'])
        ).strftime('%H:%M:%S')
        list.append(bewerk)
    return(list)

data_xml = read_xml()
Film_Name = list_titels(data_xml)
Start_Time = list_begin_time(data_xml)
End_Time = list_end_time(data_xml)
Date = datum()

#SQL PART

def SQL_Write_Films(Name_Film,Start,End,Date_of_Film):

    #SQLlite database needs to be defined
    sqlite_file = '..\db_project.sqlite'

    #initializing SQlite connector
    conn = sqlite3.connect(sqlite_file)
    c= conn.cursor()
    query = '''INSERT INTO Films (Film_Name, Start_time, End_time, Date) VALUES (?,?,?,?)''',(Film_Name,Start_Time,End_Time,Date)
    #executing query with variables that can be passed through to the function.
        # conn.execute('''INSERT INTO Films (Film_Name, Start_time, End_time, Date)
        #         VALUES (?,?,?,?)''',(Film_Name,Start_Time,End_Time,Date))
    try:
        for e in Film_Name:
            position = Film_Name.index(e)
            print(position)
            print(query)

    finally:
            conn.commit()
            conn.close()





SQL_Write_Films(Film_Name,Start_Time,End_Time,Date)
