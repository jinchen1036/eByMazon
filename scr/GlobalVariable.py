# mysql
import mysql.connector
from mysql.connector import errorcode

class globalV():
    root = None
    guest = None
    ou = None
    su = None
    general = None
    item = None
    itemList = None

    config = {
        "user": '',  # Enter your own username
        "password": '',  # Enter your own password
        "host": '127.0.0.1',
        "database": 'eByMazon'
    }

    try:
        cnx = mysql.connector.connect(**config)
        cnx.set_unicode(value=True)
        cursor = cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise err