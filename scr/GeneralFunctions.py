# Functions in this General Class
# - checkEmpty(self, input)
# - checkInt(self, input)
# - checkFloat(self, input)
# - login_check(self, username, password)
# - getID(self,username)
# - compliantCheck(self,ID)
# - checkWarning(self, id)
# - removeOU(self,username)
# - appeal(self,ouID,message)
# - ouPopularItem(self, ouID)
# - popularItem(self)
# - searchItem(self,keywords)
# - sortItem(self,items,attribute, decs)
# - checkOwner(self,ouID,itemID)
# - checkNotification(self)
# - findtaboo(self, input)

import mysql.connector
try:
    from scr.GU import GU
    from scr.Item import Item
except ModuleNotFoundError:
    from GU import GU
    from Item import Item

class General():
    def __init__(self,cursor,cnx):
        self.cnx = cnx
        self.cursor = cursor

    ################### Check FUNCTIONS ################
    def checkEmpty(self, input):
        if input is None or input == '':
            return False
        return True

    def checkInt(self, input):
        if input is None or input == '':
            return False
        try:
            int(input)
            return True
        except ValueError:
            return False

    def checkFloat(self, input):
        if input is None or input == '':
            return False
        return isinstance(input, float) or self.checkInt(input)


    ################### Login FUNCTIONS ################
    def login_check(self, username, password):
        '''
        function: check login info with DB
        :param username:
        :param password:
        :return:
            -   dict{'ID','userType','status'}  for correct login OU
            -   dict{'ID','userType'}           for correct login SU
            -   1                               for password not match
            -   2                               for in GU application
            -   3                               for in blacklist
            -   False                           nothing found
        '''
        qry = "SELECT ID, userType FROM User WHERE username=%s AND password=%s;"
        self.cursor.execute(qry,(username,password))

        user = self.cursor.fetchone()
        if user:
            if not user[1]:     # For OU
                self.compliantCheck(user[0])
                self.checkWarning(user[0])
                self.cursor.execute("SELECT status FROM OUstatus WHERE ouID = %s;" % user[0])
                return {'ID': user[0], 'userType': user[1],'status':self.cursor.fetchone()[0]}
            return {'ID': user[0], 'userType': user[1]}  # For SU

        tempGU = GU(cnx=self.cnx,cursor=self.cursor)
        return tempGU.checkUsername(username)


    def getID(self,username):
        self.cursor.execute("SELECT ID FROM User WHERE username = '%s'" % username)
        return self.cursor.fetchone()[0]

    ########################################## OU Check #########################################################
    def compliantCheck(self,ID):
        '''
        :return: check 2 justified compliants, if true add to warning DB
        '''
        qry = ("SELECT count(*) FROM Warning WHERE warningID = 1 AND ouID = %s;" % ID)
        self.cursor.execute(qry)
        count = self.cursor.fetchone()[0]

        #  check if warn not exist
        if count == 0:
            qry =("SELECT count(*) FROM Complaint NATURAL JOIN ItemOwner JOIN OUstatus ON ownerID = ouID "
                  "WHERE justified = TRUE AND ownerID = %s AND compliantTime > statusTime;" % ID)
            self.cursor.execute(qry)
            count = self.cursor.fetchone()[0]
            des = "Received %d Complain" % count
            if count >= 2:
                qry = ("INSERT INTO Warning(ouID, warningID, description) VALUES (%s, 1, '%s');" % (ID,des))
                self.cursor.execute(qry)
                self.cnx.commit()


    def checkWarning(self, id):
        qry = ("SELECT count(*) FROM Warning NATURAL JOIN OUstatus "
               "WHERE ouID = %s AND warnTime > statusTime;" % id)

        self.cursor.execute(qry)
        count = self.cursor.fetchone()[0]
        if count >= 2:
            self.cursor.execute("UPDATE OUstatus SET status = 2 WHERE ouID = %s;" % id)
            self.cnx.commit()


    def removeOU(self,username):
        """
        Remove OU from DB, and add his/her username to blacklist
        """
        try:
            qry = "DELETE FROM User WHERE username = '%s';" % username
            self.cursor.execute(qry)
            self.cursor.execute("INSERT INTO ouBlacklist VALUE ('%s');"%username)
            self.cnx.commit()
            return True
        except mysql.connector.Error as ERR:
            print("Error in Remove OU: %s"%ERR)
            return False

    def appeal(self,ouID,message):
        qry = "INSERT INTO Appeal(ouID, message) VALUES (%s,'%s');" % (ouID, message)
        try:
            self.cursor.execute(qry)
            self.cnx.commit()
        except mysql.connector.Error as err:
            print("Error in submit appeal: %s" % err)

    ############################################# Item FUNCTIONS ##########################################
    def ouPopularItem(self, ouID):
        # qry = ("SELECT itemID FROM ItemInfo NATURAL JOIN ItemView LEFT JOIN OUlike ON title LIKE CONCAT('%', keyword ,'%') AND ouID = %s WHERE saleStatus = TRUE ORDER BY OUlike.frequency DESC, ItemView.frequency DESC;")% ouID
        qry = ( "SELECT itemID FROM ItemInfo NATURAL JOIN ItemView LEFT JOIN OUlike ON title LIKE CONCAT('%', keyword ,'%')")
        qry2 = " AND ouID = %s WHERE saleStatus = TRUE ORDER BY OUlike.frequency DESC, ItemView.frequency DESC;" % ouID
        qry += qry2

        self.cursor.execute(qry)
        allItem = []
        allItems = self.cursor.fetchall()
        for info in allItems:
            allItem.append(Item(cnx=self.cnx,cursor=self.cursor,itemID=info[0]))
        return allItem

    def popularItem(self):
        """
        :return: list of Item object order by popular search keyword and view frequency
        """
        qry =("SELECT itemID FROM ItemInfo NATURAL JOIN ItemView "
              "LEFT JOIN searchKeyword ON title LIKE CONCAT('%', keyword ,'%') "
              "WHERE saleStatus = TRUE ORDER BY searchKeyword.frequency DESC, ItemView.frequency DESC;")
        self.cursor.execute(qry)
        allItem = []
        allItems = self.cursor.fetchall()
        for info in allItems:
            allItem.append(Item(cnx=self.cnx,cursor=self.cursor,itemID=info[0]))
        return allItem

    def searchItem(self,keywords):
        """
        :param keywords: search keyword
        :return:
            - False if not found, add to Notification DB
            - list of item, if found
        """

        qry = ("INSERT INTO searchKeyword(keyword) VALUES ('%s') ON DUPLICATE KEY UPDATE frequency =frequency+1;" % (keywords))
        self.cursor.execute(qry)
        self.cnx.commit()

        # qry = ("SELECT itemID FROM ItemInfo WHERE (title LIKE '%s' OR description LIKE '%s') AND saleStatus = True;"
        #        % (('%'+keywords+'%','%'+keywords+'%')))
        qry = ("SELECT itemID FROM ItemInfo WHERE title LIKE '%s' AND saleStatus = True;"
               % ('%' + keywords + '%'))
        self.cursor.execute(qry)

        allItem = []
        allItems = self.cursor.fetchall()
        if not allItems:
            self.cursor.execute("INSERT INTO Notification VALUE ('%s');"% keywords)
            self.cnx.commit()
            return False
        else:
            for info in allItems:
                allItem.append(Item(cnx=self.cnx,cursor=self.cursor,itemID=info[0]))
            return allItem


    def sortItem(self,items,attribute, decs):
        """
        :param items:  list of item object
        :param attribute:  attribute to be sort (string)
        :param decs: True for sorted in Descending order, False for ascend
        :return:
        """
        k = sorted(items, key=lambda x: getattr(x, attribute),reverse= decs)
        return k

    ############################################# Item FUNCTIONS ##########################################
    def checkOwner(self,ouID,itemID):
        qry = "SELECT EXISTS(SELECT * from ItemOwner WHERE itemID=%s AND ownerID =%s);" % (itemID, ouID)
        self.cursor.execute(qry)

        if self.cursor.fetchone()[0]:
            return False
        return True

    def checkNotification(self):
        self.cursor.execute("SELECT keyword from Notification;")
        words = ""
        for word in self.cursor:
            words += word[0]+","

        if words != "":
            words = words[:-1]
        return words
    
    def findtaboo(self, input):
        qry = "SELECT word FROM Taboo WHERE '%s' " % input
        qry2 = "LIKE CONCAT('%', word ,'%') ;" 
        self.cursor.execute(qry+qry2)

        self.taboowords =[]
        for word in self.cursor:
            self.taboowords.append(word[0])
        return self.taboowords
    # def checkStaus(self, ouID):
    #     # return status of the select OU
    #     pass

    # def changeStaus(self, ouID):
    #     #update new status
    #     # get call when receive warning or low rating
    #     pass

    # def manageWarnig(self,ouID):
    #     # called when add a warning
    #     # check number warning receive, if greater or equal to 2, suspend OU
    #     # else make sure that ou is not VIP
    #     pass

    # def ouBlacklist(self,ouID):
    #     # remove the ou from all DB and all active sale item post by that ou,
    #     # but not the sold item by he/she, the seller will be None
    #     # add the username to ouBlacklist
    #     pass


