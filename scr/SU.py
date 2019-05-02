import mysql.connector
try:
    from scr.OU import OU
    from scr.Item import Item
except ModuleNotFoundError:
    from OU import OU
    from Item import Item


class SU():
    def __init__(self,cnx, cursor,suID):
        self.cnx = cnx
        self.cursor = cursor
        self.ID = suID
    def getGU(self):
        self.cursor.execute("SELECT * FROM GUapplications;")
        self.guApplication =[]

        for gu in self.cursor:
            self.guApplication.append({'guusername':gu[0], 'guname':gu[2], 'guphone': gu[6],
                                       'guemail':gu[1], 'guaddress':gu[4],
                                       'guState': gu[5], 'gucard': gu[3]})
        return self.guApplication

    def getOU(self):
        self.cursor.execute("SELECT ouID FROM OU;")
        self.ous =[]
        ids = self.cursor.fetchall()
        for id in ids:
            self.ous.append(OU(cnx=self.cnx, cursor=self.cursor, ouID=id[0]))
        return self.ous

    def removeOU(self, ouID):
        qry = "UPDATE OUstatus SET status = 3 WHERE ouID = %s" % ouID
        self.cursor.execute(qry)
        self.cnx.commit()

    def manageApplication(self, username, action):
        # action == True: approve: register GU to OU account and delete application, set password same as username
        # action == False: decline: delete it from application accounts
        if action:
            self.cursor.execute("SELECT * FROM GUapplications WHERE username = '%s';" % username)
            info = self.cursor.fetchone()

            qry = "INSERT INTO User(username,password,userType) VALUES ('%s', '%s', %s);" % (info[0],info[0],False)
            self.cursor.execute(qry)

            self.cursor.execute("SELECT MAX(ID) FROM User;")
            ouID = self.cursor.fetchone()[0]

            qry = "INSERT INTO OU(ouID,name, cardNumber, email, address, state, phone) VALUES (%s,%s,%s,%s,%s,%s,%s);"
            self.cursor.execute(qry, (ouID, info[2],info[3],info[1],info[4],info[5],info[6]))

            qry = "INSERT INTO OUstatus(ouID) VALUES (%s);" % ouID
            self.cursor.execute(qry)

        self.cursor.execute("DELETE FROM GUapplications WHERE username = '%s';" % username)
        self.cnx.commit()

    def getAllItem(self):
        qry = "SELECT itemID FROM ItemOwner NATURAL JOIN ItemInfo;"
        self.cursor.execute(qry)
        self.items = []
        allitem = self.cursor.fetchall()
        for item in allitem:
            self.items.append(Item(cnx=self.cnx, cursor=self.cursor,itemID=item[0]))
        return self.items

    def manageItem(self, itemID, action, justification='removed By SU'):
        # action == True: approve: change approvalStatus in ItemDB to True
        # action == False: decline: remove the item in ItemDB, add warning to post OU in warningDB
        if not action:      #decline
            self.removeItem(itemID,justification)
        else:               # approve
            self.cursor.execute("UPDATE ItemInfo SET saleStatus = True, approvalStatus = True WHERE itemID = %s;" % itemID)
        self.cnx.commit()

    def removeItem(self,itemID, justification='removed By SU'):
        # remove all the occurance of this item in DB
        # add to Blacklist and warning to owner
        item = Item(self.cnx, self.cursor, itemID)
        # add warning
        self.cursor.execute("INSERT INTO Warning(ouID,warningID,description) VALUE (%s,3,'%s')"
                            % (item.owner,str(itemID)+'_'+justification))
        # Blacklist Item
        self.cursor.execute("INSERT INTO itemBlackList(itemID,title) VALUE (%s,'%s');"
                            % (item.itemID,item.title))
        # Delete Item
        self.cursor.execute("DELETE FROM ItemInfo WHERE itemID = %s;" % itemID)
        self.cnx.commit()

    def viewCompliant(self):
        # Get all compliant from DB, return array of dict{itemID, complianerID, description, compliantTime}
        pass

    def manageCompliant(self, itemID, complianerID, action):
        # action == True: remove: delete compliant in DB
        # action == False: justified: change the justified to True in DB
        #                  check for two justified compliant that will cause warning
        pass

    def getTabooList(self):
        self.cursor.execute("SELECT * FROM Taboo;")
        self.tabooList = []

        for taboo in self.cursor:
            self.tabooList.append({'taboo': taboo[0]})
        return self.tabooList

    def getTransaction(self):
        self.cursor.execute("SELECT * FROM Transaction NATURAL JOIN ItemOwner ORDER BY dealTime DESC;")
        self.OUtransactions = []

        for transaction in self.cursor:
            self.OUtransactions.append({'sellerID': transaction[7], 'itemID': transaction[0],
            'buyerID':transaction[1],'price':round(transaction[3],2),'shipping': transaction[5],
            'date': transaction[6].strftime("%m/%d/%Y") }) #to be fixed(query)
            # print(transaction)
        return self.OUtransactions

    def getUserBlackList(self):
        self.cursor.execute("SELECT * FROM ouBlacklist;")
        self.userBlackList = []

        for user in self.cursor:
            self.userBlackList.append({'username': user[0]})

        return self.userBlackList

    def getItemBlackList(self):
        self.cursor.execute("SELECT * FROM itemBlackList NATURAL JOIN ItemOwner;")
        self.itemBlackList = []

        for item in self.cursor:
            self.itemBlackList.append({'ownerID':str(item[2]),'itemID': str(item[0]), 'itemTitle':item[1]})

        return self.itemBlackList

    def addTaboo(self, taboo):
        qry = ("INSERT INTO Taboo(word) VALUES ('%s');" %taboo)
        try:
            self.cursor.execute(qry)
            self.cnx.commit()
            return True
        except mysql.connector.errors as ERR:
            print(ERR)
            return False