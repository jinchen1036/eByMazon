# Functions in this SU Class
# - getGU(self)
# - manageApplication(self, username, action)
# - getOU(self)
# - getAppeal(self)
# - deleteAppeal(self,ouID)
# - acceptAppeal(self,ouID)
# - removeOU(self, ouID)
# - getAllItem(self)
# - manageItem(self, itemID, action, justification='item removed By SU')
# - removeItem(self,itemID, justification='item removed By SU')
# - viewCompliant(self)
# - manageCompliant(self, itemID, complianerID, action)
# - getTransaction(self)
# - getUserBlackList(self)
# - getItemBlackList(self)
# - getTabooList(self)
# - addTaboo(self, taboo)

import mysql.connector
import datetime
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

    ########################################## GU Management ###############################################
    def getGU(self):
        '''
        :return: initial  self.guApplication
            self.guApplication -> list of dict{guusername,guname,guphone,guemail,guaddress,guState,gucard}
        '''
        self.cursor.execute("SELECT * FROM GUapplications;")
        self.guApplication =[]

        for gu in self.cursor:
            self.guApplication.append({'guusername':gu[0], 'guname':gu[2], 'guphone': gu[6],
                                       'guemail':gu[1], 'guaddress':gu[4],
                                       'guState': gu[5], 'gucard': gu[3]})
        return self.guApplication

    def manageApplication(self, username, action):
        '''
        :param username: gu applicant's username
        :param action(bool):
                if True approve: register GU to OU account and delete application, set password same as username
                if False decline: delete it from application accounts
        '''
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

    ########################################## OU Management ###############################################
    def getOU(self):
        '''
        :return: initial self.ous
            self.ous -> list of OU object
        '''
        self.cursor.execute("SELECT ouID FROM OU;")
        self.ous =[]
        ids = self.cursor.fetchall()
        for id in ids:
            self.ous.append(OU(cnx=self.cnx, cursor=self.cursor, ouID=id[0]))
        return self.ous

    def getAppeal(self):
        '''
        :return: initial self.appeals
            self.appeals -> list of dict{ouID,message,time}
        '''
        self.cursor.execute("SELECT * FROM Appeal;")
        self.appeals =[]
        ids = self.cursor.fetchall()
        for id in ids:
            self.appeals.append({'ouID':id[0], 'message':id[1], 'time':id[2].strftime("%m/%d/%Y")})
        return self.appeals

    def deleteAppeal(self,ouID):
        '''
        :param ouID: ou's appeal to be delete
        '''
        self.cursor.execute("DELETE FROM Appeal WHERE ouID = %s;"% ouID)
        self.cnx.commit()

    def acceptAppeal(self,ouID):
        '''
        :param ouID: ou's appeal to be approve
        '''
        self.cursor.execute("UPDATE OUstatus SET status = 0, statusTime = '%s' WHERE ouID = %s;" % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ouID))
        self.deleteAppeal(ouID)

    def removeOU(self, ouID):
        '''
        :param ouID: ou to be remove
        '''
        qry = "UPDATE OUstatus SET status = 3 WHERE ouID = %s;" % ouID
        self.cursor.execute(qry)


        self.cursor.execute("SELECT username FROM User WHERE ID = %s" %ouID)

        username = self.cursor.fetchone()[0]
        self.cursor.execute("INSERT INTO ouBlacklist VALUE ('%s');" % username)

        self.cnx.commit()

    ########################################## Item Management ###############################################
    def getAllItem(self):
        '''
        :return: initial self.items
            self.items -> list of Item object
        '''
        qry = "SELECT itemID FROM ItemOwner NATURAL JOIN ItemInfo;"
        self.cursor.execute(qry)
        self.items = []
        allitem = self.cursor.fetchall()
        for item in allitem:
            self.items.append(Item(cnx=self.cnx, cursor=self.cursor,itemID=item[0]))
        return self.items

    def manageItem(self, itemID, action, justification='item removed By SU'):
        '''
        :param itemID: item to be approve or decline
        :param action(bool):
            if True approve: change approvalStatus in ItemDB to True, check with notificationDB for any keyword remove
            if False decline: remove the item in ItemDB, add warning to post OU in warningDB
        :param justification:
            need if decline, default 'itemremoved By SU'
        '''

        if not action:      #decline
            self.removeItem(itemID,justification)
        else:               # approve
            self.cursor.execute("UPDATE ItemInfo SET saleStatus = True, approvalStatus = True WHERE itemID = %s;" % itemID)

            self.cursor.execute("SELECT title FROM ItemInfo WHERE itemID = %s;" % itemID)
            title = self.cursor.fetchone()[0]

            # Remove keyword from notification DB
            qry = "DELETE FROM Notification WHERE '%s' "% title
            qry += " LIKE CONCAT('%', keyword ,'%') ;"
            self.cursor.execute(qry)

        self.cnx.commit()


    def removeItem(self,itemID, justification='item removed By SU'):
        '''
        :param itemID: item to be remove
        :param justification: note from su reason, default: 'item removed By SU'
        :return:
            remove all the occurance of this item in DB
            add to Blacklist and warning to owner
        '''

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


    ########################################## Complain Management ###############################################
    def viewCompliant(self):
        '''
        :return: initial self.compliants
            self.compliants -> list of dict{itemID, complianerID, description, compliantTime}
        '''

        self.cursor.execute("SELECT * FROM Complaint NATURAL JOIN ItemOwner ORDER BY justified;")
        self.compliants = []
        for compliant in self.cursor:
            self.compliants.append({'ownerID': compliant[5],'itemID':compliant[0],
                                    'complainerID':compliant[1],'complain':compliant[2],
                                    'time':compliant[3].strftime("%m/%d/%Y"),'justified': compliant[4]})
        return self.compliants

    def manageCompliant(self, itemID, complianerID, action):
        '''
        :param itemID: item with that complain
        :param complianerID: complainer id
        :param action:
            if True: remove: delete compliant in DB
            if False: justified: change the justified to True in DB
        :return:
        '''
        if action:
            self.cursor.execute("UPDATE Complaint SET justified = TRUE WHERE itemID = %s AND complainerID = %s;" %(itemID,complianerID))

        # check warning during ou login
        else:
            self.cursor.execute("DELETE FROM Complaint WHERE itemID = %s AND complainerID = %s;" % (itemID, complianerID))
        self.cnx.commit()

    ########################################## Other Management ###############################################
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
        # Return list of dict{'username'} in ouBlacklist
        self.cursor.execute("SELECT * FROM ouBlacklist;")
        self.userBlackList = []

        for user in self.cursor:
            self.userBlackList.append({'username': user[0]})

        return self.userBlackList

    def getItemBlackList(self):
        # Return list of dict{'ownerID', 'itemID', 'itemTitle'} in the itemBlackList
        self.cursor.execute("SELECT * FROM itemBlackList NATURAL JOIN ItemOwner;")
        self.itemBlackList = []

        for item in self.cursor:
            self.itemBlackList.append({'ownerID':str(item[2]),'itemID': str(item[0]), 'itemTitle':item[1]})

        return self.itemBlackList


    def getTabooList(self):
        # Return list of dict{'taboo'} in the taboo DB
        self.cursor.execute("SELECT * FROM Taboo;")
        self.tabooList = []
        tabooDict = []
        for taboo in self.cursor:
            self.tabooList.append(taboo[0].upper())
            tabooDict.append({'taboo': taboo[0]})
        return tabooDict

    def addTaboo(self, taboo):
        '''
        :param taboo: a string of taboo word
        :return: True if insert sucessfully, False if insert false
        '''
        if taboo.upper() in self.tabooList:
            return False

        qry = ("INSERT INTO Taboo(word) VALUES ('%s');" % taboo)
        try:
            self.cursor.execute(qry)
            self.cnx.commit()
            return True
        except mysql.connector.errors as ERR:
            print(ERR)
            return False