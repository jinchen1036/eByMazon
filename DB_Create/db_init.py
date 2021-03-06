# If you don't have mysql.connect library
# Run `pip install mysql-connector` to install

import mysql.connector
from mysql.connector import errorcode, OperationalError

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
        # file.write(data.decode('base64'))

def insertItemInfo(cursor, itemID, image, title,description, priceType, saleStatus,approvalStatus):
    try:
        image = convertToBinaryData('./' + image)
    except FileNotFoundError:
        image = convertToBinaryData('DB_Create/' + image)
    try:

        qry = ("INSERT INTO ItemInfo(itemID, image, title, description, priceType, saleStatus,approvalStatus) "
               "VALUE (%s,%s,%s,%s,%s,%s,%s)"
               "ON DUPLICATE KEY UPDATE "
               "image=%s, title=%s, description = %s, priceType=%s, saleStatus=%s,approvalStatus =%s;")
        result = cursor.execute(qry, (itemID,image,title,description,priceType, saleStatus,approvalStatus,
                                      image
                                      ,title,description,priceType, saleStatus,approvalStatus))
        cnx.commit()
    except mysql.connector.Error as err:
        print("Error in insert item info to database")
        print(err)

def getItemInfo(cursor, itemID):
    try:
        qry = "SELECT image FROM ItemInfo WHERE itemID = %s;"%itemID
        cursor.execute(qry, (itemID))
        for image in cursor:
            write_file(image[0],'test.jpg')
    except mysql.connector.Error as err:
        print("Error in getting item info to database")
        print(err)


def executeScriptsFromFile(cnx, cursor,filename):
    # Open and read the file as a single buffer
    try:
        fd = open('./' + filename, 'r')
    except FileNotFoundError:
        fd = open('DB_Create/' + filename, 'r')

    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')


    for command in sqlCommands:
        try:
            cursor.execute(command)
            cnx.commit()
        except mysql.connector.errors.ProgrammingError as err:
            print(err)
        # except OperationalError:
        #     print("Command skipped: ")


if __name__  == "__main__":
    config = {
        "user": '',                 # Enter your own username
        "password": '',             # Enter your own password
        "host": '127.0.0.1',
        # "database": 'eByMazon'
    }

    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise err



    # Create relations in DB
    print("Create eByMazon")
    executeScriptsFromFile(cnx, cursor, 'schema.sql')
    # If take to long to run this command, means you didn't fully close all the connection of this database,
    # Run below code in terminal:
        #   mysqladmin processlist -u username -p            -- replace your own username with the username
        #   mysqladmin kill id -u username -p                -- replace the id with the process id of your database



    # Insert values to other tables
    print("Insert Values to eByMazon")
    executeScriptsFromFile(cnx,cursor,'insertValues.sql')


    # Insert State Sale Tax Rates
    print("Insert State Sale Tax Rates")
    executeScriptsFromFile(cnx,cursor,'Insert_Taxes_Rate.sql')

    # Insert Item info
    # Maximum size currently an image can have is 64KB
    # insertItemInfo(cursor, itemID, image, title,description, priceType,usedStatus, saleStatus)
    print("Insert Item Info")
    insertItemInfo(cursor, itemID=1,image="images/item1.jpg",title="SHE Forever CD",
                   description="New Song + Collection, released on 21 July 2006 by HIM International Music",
                   priceType=False, saleStatus=True,approvalStatus=True)
    insertItemInfo(cursor,itemID=2, image="images/item2.jpg",title="SHE Shero DVD",description = "DVD for concert",
                   priceType=False, saleStatus=True,approvalStatus=True)
    insertItemInfo(cursor,itemID=3,image="images/item3.jpg",title="Harry Potter Book Series",
                   description="Author: J. K. Rowling. Include The Philosopher's Stone. (1997), \nThe Chamber of Secrets. (1998),"
                   "The Prisoner of Azkaban. (1999),\nThe Goblet of Fire. (2000), The Order of the Phoenix. (2003),\n"
                   "The Half-Blood Prince. (2005),The Deathly Hallows. (2007)",
                   priceType=False,  saleStatus=False,approvalStatus=False)
    insertItemInfo(cursor,itemID=4,image="images/item4.jpg",title="The Hunger Games",
                   description="2008 dystopian novel by the American writer Suzanne Collins.",
                   priceType=False, saleStatus=False,approvalStatus=False)
    insertItemInfo(cursor,itemID=5,image="images/item5.jpg",title="Samsung 17-Inch Laptop",
                   description="17-Inch Series 7 Chronos Laptop.\n Used a year, still in good condition, Bright and vivid display; \n Good JBL speakers; Long battery life",
                   priceType=True,saleStatus=True,approvalStatus=True)
    insertItemInfo(cursor,itemID=6,image="images/item6.jpg",title="Macbook Air 13-Inch",description="Used 2 year, early 2015 version.\n"
                    "1.8GHz dual-core Intel Core i5 processor,\n Turbo Boost up to 2.9GHz,\n128GB SSD storage",
                   priceType=True,  saleStatus=True,approvalStatus=True)

    insertItemInfo(cursor,itemID=7,image="images/item7.jpg",title="Woman Eye Glass",description="Plastic frame and lens.\nNon-polarized",
                   priceType=False,  saleStatus=True,approvalStatus=True)
    insertItemInfo(cursor,itemID=8,image="images/item8.jpg",title="Wilson Basketball",description="Best combination of grip and durability.\nApproved for play by the NFHS",
                   priceType=False,  saleStatus=False,approvalStatus=False)
    insertItemInfo(cursor,itemID=9,image="images/item9.jpg",title="Women Citizen Watch",description="Stainless steel bracelet\nWater resistant to 100 m",
                   priceType=True,  saleStatus=True,approvalStatus=True)
    insertItemInfo(cursor,itemID=10,image="images/item10.jpg",title="Jo Malone Perfume",description="2.4 oz Cologne Spray.\nNectarine Blossom & Honey Cologne",
                   priceType=False,  saleStatus=True,approvalStatus=True)
    insertItemInfo(cursor,itemID=11,image="images/item11.jpg",title="Bueno Chocolate",description="Delicious kinder milk chocolate.\nTotal 9 Bar\n Weight 1.5 oz per bar",
                   priceType=False,  saleStatus=True,approvalStatus=True)
    insertItemInfo(cursor,itemID=12,image="images/item12.jpg",title="Reloaded CD",description="Luhan's first studio album.\nReleased on December 14, 2015",
                   priceType=False,  saleStatus=True,approvalStatus=True)
    # Insert values to other tables
    print("Insert Item to eByMazon")
    executeScriptsFromFile(cnx,cursor,'insertItem.sql')
    cnx.commit()        #Need to make sure everything push to database

# Test get image
# getItemInfo(cursor, 1)
# print()
