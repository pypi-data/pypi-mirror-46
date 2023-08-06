from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sys
import requests 
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def get_redirect_url(url):
    r = requests.get(url)
    return r.url


def simple_update_or_create(mydb,keys,table,valDictionary):
        mycursor = mydb.cursor()
        tries=3
        while tries > 0:
                tries -= 1
                try:
                        keyString=""
                        for keyColumn in keys.keys():
                            keyString= keyString + " " + keyColumn + "=\"" + str(keys.get(keyColumn))+"\""
                        checkIfKeyExists="select count(*) from " + table + " where" + keyString
                        #print(checkIfKeyExists)
                        mycursor.execute(checkIfKeyExists)
                        matchingValues= mycursor.fetchall()[0][0]
                        #print("maching lines " + str(matchingValues))
                        if matchingValues == 0:
                            # CREATE
                            for keyColumn in keys.keys():
                                valDictionary[keyColumn]=str(keys.get(keyColumn))
                                #print(valDictionary)
                                simple_insert(mydb,'insert',table,valDictionary)
                                print("CREATED")

                        if matchingValues == 1:
                            # UPDATE
                            sqlUpdate="update "+table+ " set"
                            firstLoop=True
                            for fields in valDictionary.keys():
                                if firstLoop == True:
                                    sqlUpdate = sqlUpdate + " " + fields +"=\""+str(valDictionary.get(fields))+"\""
                                    firstLoop=False
                                else:
                                    sqlUpdate = sqlUpdate + ", " + fields +"=\""+str(valDictionary.get(fields))+"\""
                            sqlUpdate = sqlUpdate + " WHERE"
                            firstLoop=True
                            for keyColumn in keys.keys():
                                if firstLoop==True:
                                    sqlUpdate = sqlUpdate + " " + keyColumn +"=\""+str(keys.get(keyColumn))+"\""
                                else:
                                    sqlUpdate = sqlUpdate + " AND " + keyColumn +"=\""+str(keys.get(keyColumn))+"\""
                            #print(sqlUpdate)
                            mycursor.execute(sqlUpdate)
                            print("UPDATED")
                        if matchingValues > 1:
                            print("[no add error] more then one match")
                            

                        break
                except Exception as e:
                        if tries == 0:
                                #print(sqlQuery)
                                print("[No add error] Failed inserting data after retrying. Error message:"+str(e))
                        else:
                                print("Reconnecting..")
                                mydb.reconnect()
    


def simple_insert(mydb, insertMethod, table, valDictionary):
        mycursor = mydb.cursor()
        tries=3
        while tries > 0:
                tries -= 1
                try:
                        columns=""
                        data=""
                        dataValues=[]
                        for key in valDictionary.keys():
                                columns+='`'+key+'`,'
                                data+='%s,'
                                dataValues.append(valDictionary.get(key))
                        sqlQuery="%s into %s (%s) VALUES (%s)" % (insertMethod, table, columns[:-1], data[:-1])
                        #print(sqlQuery)
                        #print(dataValues)
                        mycursor.execute(sqlQuery,dataValues)
                        mydb.commit()
                        print("Data Updated!")
                        break
                except Exception as e:
                        if tries == 0:
                                #print(sqlQuery)
                                print("[No add error] Failed inserting data after retrying. Error message:"+str(e))
                        else:
                                print("Reconnecting..")
                                mydb.reconnect()

def simple_createstatement(tableName, valDictionary):
        sqlQuery='CREATE TABLE '+tableName+ ' ('
        sqlQuery+=''.join(key+' VARCHAR(255), ' for key in valDictionary.keys())
        sqlQuery=sqlQuery[:-2]
        sqlQuery+=');'
        print(sqlQuery)


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
#    content_type = resp.headers['Content-Type'].lower()
#    return (resp.status_code == 200 
#            and content_type is not None)
    return (resp.status_code == 200)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)
