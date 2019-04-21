import mysql.connector
from kivy.core.image import Image as CoreImage
from io import BytesIO
try:
    from scr.GU import GU
except ModuleNotFoundError:
    from GU import GU
class General():
    def __init__(self,cursor,cnx):
        self.cnx = cnx
        self.cursor = cursor

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
                self.cursor.execute("SELECT status FROM OUstatus WHERE ouID = %s;" % user[0])
                return {'ID': user[0], 'userType': user[1],'status':self.cursor.fetchone()[0]}
            return {'ID': user[0], 'userType': user[1]}  # For SU

        tempGU = GU(cnx=self.cnx,cursor=self.cursor)
        return tempGU.checkUsername(username)



    def removeOU(self,ouID,username):
        """
        Remove OU from DB, and add his/her username to blacklist
        """
        try:
            self.cursor.execute("DELETE FROM User where ID = %s;"% ouID)
            self.cursor.execute("INSERT INTO ouBlacklist VALUE ('%s');"%username)
            self.cnx.commit()
            return True
        except mysql.connector.Error as ERR:
            print("Error in Remove OU: %s"%ERR)
            return False

    def getItemInfo(self, itemID):
        try:
            qry = "SELECT * FROM ItemInfo WHERE itemID = %s;" % itemID
            self.cursor.execute(qry, (itemID))


        except mysql.connector.Error as err:
            print("Error in getting item info to database")
            print(err)

    def popularItem(self):
        qry = "SELECT itemID, image, title, description, priceType, usedStatus FROM ItemInfo WHERE saleStatus = True;"
        self.cursor.execute(qry)
        allItem = []
        for info in self.cursor:
            # print(type(info[1]))

            # data = BytesIO(info[1])
            used,priceType = "No","FixedPrice"
            if info[4]:
                priceType="Bidding"
            if info[5]:
                used = "Yes"

            information = 'Price Type: '+priceType +'\nUsed Status:'+used
            allItem.append({"itemID":info[0],"image":CoreImage(BytesIO(info[1]), ext="png").texture,"title":info[2],
                            "priceType":info[4],"info":information,"description":info[3]})
        return allItem

    def checkStaus(self, ouID):
        # return status of the select OU
        pass

    def changeStaus(self, ouID):
        #update new status
        # get call when receive warning or low rating
        pass

    def manageWarnig(self,ouID):
        # called when add a warning
        # check number warning receive, if greater or equal to 2, suspend OU
        # else make sure that ou is not VIP
        pass

    def ouBlacklist(self,ouID):
        # remove the ou from all DB and all active sale item post by that ou,
        # but not the sold item by he/she, the seller will be None
        # add the username to ouBlacklist
        pass

    def itemBlacklist(self,itemID):
        # remove all the occurance of this item in DB
        # add to itBlacklist
        pass
