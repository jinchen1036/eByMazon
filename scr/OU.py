
import datetime
import mysql.connector

try:
    from scr.Item import Item
except ModuleNotFoundError:
    from Item import Item

class OU():
    def __init__(self,cnx, cursor,ouID):
        self.cursor = cursor
        self.cnx = cnx
        self.ID = ouID
        self.getOUInfo()
        self.getItem()
        self.getCompliants()

    ####################### Get Info #####################################
    def getOUInfo(self):
        # Get ou information in strings: name, card number, address, state, phone
        self.cursor.execute("SELECT * FROM OU WHERE ouID = %s"% self.ID)

        for info in self.cursor:
            self.name, self.card, self.email= info[1],info[2],info[3]
            self.address, self.state, self.phone = info[4],info[5],info[6]

        self.cursor.execute("SELECT * FROM OUstatus WHERE ouID = %s" % self.ID)
        for status in self.cursor:
            self.moneySpend, self.avgRate, self.status,self.statusTime= status[1],status[2],status[3],status[4]

        self.getTax()


    def getItem(self):
        ''' Get items that own by current OU, in list of Item class '''

        qry = "SELECT itemID FROM ItemOwner NATURAL JOIN ItemInfo WHERE ownerID = %s;" % self.ID
        self.cursor.execute(qry)
        self.items = []

        allitem = self.cursor.fetchall()
        for item in allitem:
            self.items.append(Item(cnx=self.cnx, cursor=self.cursor,itemID=item[0]))
        return self.items

    def getTax(self):
        qry = "SELECT taxRate FROM Tax WHERE state = '%s';" % self.state
        self.cursor.execute(qry)
        self.taxRate = self.cursor.fetchone()[0]

    def getCompliants(self):
        qry =("SELECT * FROM Complaint NATURAL JOIN ItemOwner "
              "WHERE justified = TRUE AND ownerID = %s;"% self.ID)
        self.cursor.execute(qry)
        self.compliants = []
        for compliant in self.cursor:
            self.compliants.append({'itemID':compliant[0], 'description': compliant[1],
                                    'compliantTime': compliant[2]})
            print(self.ID, self.name, compliant[0])



    ####################### Change Info #####################################
    def changePassword(self,password):
        #update password in DB
        qry = "UPDATE User SET password = %s WHERE ID = %s;"
        try:
            self.cursor.execute(qry, (password,self.ID))
            self.cnx.commit()
            return True
        except mysql.connector.errors:
            print("Error in update OU password")
            return False

    def updateOUInfo(self, name, card, email,phone, address, state):
        # update OU info in DB
        qry = "UPDATE OU SET name = %s, cardNumber= %s, email=%s,address =%s, state =%s, phone=%s WHERE ouID=%s;"

        try:
            self.cursor.execute(qry,(name, card,email,address,state,phone,self.ID))
            self.cnx.commit()
            self.getOUInfo()    #update info
            return True

        except mysql.connector.errors:
            print("Error in update OU Info")
            return False

    ####################### Search Info #####################################
    def searchAdd(self,keyword):
        qry = ("INSERT INTO OUlike(ouID, keyword) VALUES (%s,'%s') ON DUPLICATE KEY UPDATE frequency =frequency+1;" %(self.ID,keyword))
        self.cursor.execute(qry)
        self.cnx.commit()


    ####################### Friend Info #####################################
    def getFriend(self):
        self.friends=[]
        qry = ("SELECT friendID,discount,username FROM FriendList JOIN User ON friendID=ID WHERE ownerID = %s;") %self.ID
        self.cursor.execute(qry)
        for info in self.cursor:
            self.friends.append({"friendID": info[0],"discount": info[1],"username": info[2]})
        return self.friends

    def getFriendMessage(self,friendID):
        qry = ("SELECT message, sendTime FROM MessageSent WHERE senderID = %s AND receiverID = %s;" % (self.ID,friendID))
        self.cursor.execute(qry)

        messages = []
        for message in self.cursor:
            messages.append({'send':True,'message': message[0],'sendTime': message[1]})

        qry = ("SELECT message, sendTime FROM MessageSent WHERE senderID = %s AND receiverID = %s;" % (friendID,self.ID))
        self.cursor.execute(qry)
        for message in self.cursor:
            messages.append({'send':False,'message': message[0],'sendTime': message[1]})

        self.messages = sorted(messages, key=lambda k: k['sendTime'])
        return self.messages

    def sendFriendMessage(self,friendID,message):
        qry = "INSERT INTO MessageSent(senderID,receiverID,message) VALUES (%s,%s,%s);"
        try:
            self.cursor.execute(qry, (self.ID, friendID, message))
            self.cnx.commit()
            return True
        except mysql.connector.errors as ERR:
            print("Error in send Friend Message %s" % ERR)
            return False


    def deleteFriend(self, friendID):
        qry = "DELETE FROM FriendList WHERE ownerID=%s AND friendID = %s;"
        try:
            self.cursor.execute(qry, (self.ID, friendID))
            self.cnx.commit()
            return True
        except mysql.connector.errors as ERR:
            print("Error in delete Friend %s" % ERR)
            return False


    def addFriend(self,friendID,discount = 0.05):
        # add friend relation to DB,
        # each friend can have customer discount, if not provide, default is 5%
        qry = "INSERT INTO FriendList(ownerID, friendID, discount) VALUES (%s,%s,%s);"
        try:
            self.cursor.execute(qry, (self.ID, friendID,discount))
            self.cnx.commit()
            return True
        except mysql.connector.errors as ERR:
            print("Error in add Friend %s" % ERR)
            return False


    ####################### Submit Item #####################################
    def submitItem(self):
        # add submit item to ItemOwner,ItemView
        # return itemID
        try:
            qry = "INSERT INTO ItemOwner(ownerID) VALUES (%s);"%self.ID
            self.cursor.execute(qry)
            self.cnx.commit()

            self.cursor.execute("SELECT MAX(itemID) FROM ItemOwner;")
            for number in self.cursor:
                iID = number[0]
            # itemID = self.cursor.fetclone()

            qry = "INSERT INTO ItemView(itemID) VALUE (%s);" % int(iID)
            self.cursor.execute(qry)
            self.cnx.commit()
            return iID
        except mysql.connector.errors as ERR:
            print(ERR)
            return False

    def submitBiddingItem(self,image, title, description, usedStatus, startPrice, endDay):
        try:
            itemID = self.submitItem()
            qry = ("INSERT INTO ItemInfo(itemID, image, title, description, priceType) "
                   "VALUE (%s,%s,%s,%s,%s);")
            self.cursor.execute(qry,(itemID,image,title,description,True))
            self.cnx.commit()

            endDay = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=endDay),
                                                     datetime.time(23, 59,59))
            qry = "INSERT INTO ItemBid(itemID, startPrice,usedStatus,endDay) VALUE (%s,%s,%s,%s);"
            self.cursor.execute(qry, (itemID, float(startPrice), usedStatus, endDay))
            self.cnx.commit()
        except mysql.connector.errors as ERR:
            print(ERR)
            return False

    def submitFixedPriceItem(self,image, title, description, price,available):
        try:
            itemID = self.submitItem()
            qry = ("INSERT INTO ItemInfo(itemID, image, title, description, priceType) "
                   "VALUE (%s,%s,%s,%s,%s);")
            self.cursor.execute(qry, (itemID,image,title,description,False))
            self.cnx.commit()

            qry = "INSERT INTO FixedPrice(itemID, price,availableNum) VALUE (%s,%s,%s);"
            self.cursor.execute(qry , (itemID, float(price), int(available)))
            self.cnx.commit()
        except mysql.connector.errors as ERR:
            print(ERR)
            return False


    ####################### Purchase Item #####################################


    def checkFriendDiscount(self,itemID):
        """
        :param itemID: item want to purchase
        :return: 0 if not friend
                discount rate if friend
        """
        qry = ("SELECT discount FROM ItemOwner NATURAL JOIN FriendList WHERE itemID = %s AND friendID = %s;" %(itemID, self.ID))
        self.cursor.execute(qry)
        discount = self.cursor.fetchone()[0]
        return 0 if discount is None else discount


    def calculatePurchase(self, itemID, price, numWant=1):
        """
        :param itemID: item want to purchase
        :return: list of [basePrice, taxAmount, deductFriend,deductVIP,finalPrice]
        """
        basePrice = price*numWant

        friendDiscount =  self.checkFriendDiscount(itemID)
        vipDiscount = 0.05 if self.status == 1 else 0

        deductF = basePrice * friendDiscount
        deductV = basePrice * vipDiscount
        taxAmount = basePrice * self.taxRate
        finalPrice = basePrice + taxAmount - deductF - deductV

        return [basePrice, taxAmount, deductF,deductV,finalPrice]



    def bidding(self,itemID, bidderID, price):
        # record bidding in BidRecord
        pass

    def purchaseFixedPrice(self, itemID, buyerID, numBuy):
        # get price from itemDB by itemID
        # get finalPrice by call self.calculateTotal
        # add to transactionDB and update buyer money spend
        pass

    def purchaseBidding(self, itemID):
        # get called when reach to the endDay of bidding
        # get second highest bidder from BidRecordDB
        # get finalPrice by call self.calculateTotal
        # add to transactionDB and update buyer money spend
        pass

    def declineTransaction(self, itemID, buyerID):
        # No available if the shipping status is true for item
        # Else: remove from transaction, deduct moneyspend from buyer status
        # Add warning to OU
        pass
        
##_____to be filled____#
    def viewTransactionHistory1(self,ouID):
        # bought
        # get transaction History from DB
        # Separate for sell and purchase, return dict{'sell','buy'}
        # each is list of transaction in form[itemID, buyerID, priceDeal, dealTime]
        # self.cursor.execute("SELECT * FROM Transaction;")
        # self.transactions = []
        # for transaction in self.cursor:
        #     self.transactions.append({'numb': str(transaction[1]), 'itemID': str(transaction[1]),
        #     'seller':str(transaction[1]), 'buyer':str(transaction[1]),'price':str(transaction[1]),
        #     'date': str(transaction[1]) }) #to be fixed(query)
        #     print(transaction)
        # return self.transactions
        pass
    def viewTransactionHistory2(self,ouID):
        # sold
        # get transaction History from DB
        # Separate for sell and purchase, return dict{'sell','buy'}
        # each is list of transaction in form[itemID, buyerID, priceDeal, dealTime]
        pass

    def submitRating(self,itemID, raterID, rating):
        # add rating to DB
        # check for bad rating that will cause warning or depromotion
        # check for good rating that will cause promotion
        pass

    def submitCompliant(self,itemID, complianterID, description):
        # add compliant to DB
        pass

    def getComplaints(self):
        self.cursor.execute("SELECT itemID, description, compliantTime FROM Complaint NATURAL JOIN ItemOwner WHERE ownerID = %s;"% self.ID)
        self.complaintList = []

        for complaint in self.cursor:
            self.complaintList.append({"itemID": complaint[0],"description":complaint[1],
                                      "compliantTime":complaint[2]})
        return self.complaintList

    def getWarnings(self):
        self.cursor.execute("SELECT warningID, description, warnTime FROM Warning WHERE ouID = %s;" % self.ID)
        self.warningList = []

        for warning in self.cursor:
            self.warningList.append({'warningID': warning[0], 'description':warning[1],
                                      'warnTime':warning[2]})
        return self.warningList