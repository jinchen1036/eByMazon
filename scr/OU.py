# Functions in this OU Class
# - getOUInfo(self)
# - getTax(self)
# - getItem(self)
# - getComplaints(self)
# - vipCheck(self)
# - biddingCheck(self)
# - changePassword(self,password)
# - updateOUInfo(self, name, card, email,phone, address, state)
# - searchAdd(self,keyword)
# - getFriend(self)
# - getFriendMessage(self,friendID)
# - sendFriendMessage(self,friendID,message)
# - deleteFriend(self, friendID)
# - addFriend(self,friendID,discount = 0.05)
# - submitItem(self)
# - insertView(self, itemID)
# - submitBiddingItem(self,image, title, description, usedStatus, startPrice, endDay)
# - submitFixedPriceItem(self,image, title, description, price,available)
# - checkFriendDiscount(self,itemID)
# - calculatePurchase(self, itemID, price, numWant=1)
# - bidding(self,itemID, price)
# - purchaseFixedPrice(self, itemID, singlePrice, numBuy,numLeft)
# - purchaseBidding(self, itemID)
# - getBidRecord(self)
# - getBuyHistory(self)
# - getSaleHistory(self)
# - acceptSale(self,itemID, buyerID, price)
# - declineSale(self,itemID, buyerID)
# - submitRating(self,itemID, rating,description)
# - submitCompliant(self,itemID, description)
# - getWarnings(self)
# - ratingCheck(self)

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
        self.promote = False
        self.depromote = False
        self.vipCheck()


        self.getOUInfo()
        self.getItem()
        self.biddingCheck()
        self.getComplaints()
        self.getWarnings()

    ####################### Get Info #####################################
    def getOUInfo(self):
        """
        :return: initalized self.variables:
            - name,card,email,address,state,phone,moneySpend,avgRate,status,taxRate
        """
        # Get ou information in strings: name, card number, address, state, phone
        self.cursor.execute("SELECT * FROM OU WHERE ouID = %s"% self.ID)

        for info in self.cursor:
            self.name, self.card, self.email= info[1],info[2],info[3]
            self.address, self.state, self.phone = info[4],info[5],info[6]

        self.cursor.execute("SELECT * FROM OUstatus WHERE ouID = %s" % self.ID)
        for status in self.cursor:
            self.moneySpend, self.avgRate, self.status,self.statusTime= status[1],status[2],status[3],status[4]

        self.getTax()

    def getTax(self):
        qry = "SELECT taxRate FROM Tax WHERE state = '%s';" % self.state
        self.cursor.execute(qry)
        self.taxRate = self.cursor.fetchone()[0]

    def getItem(self):
        '''
        :return: self.items
            self.items - list of item object owned by current OU object
        '''

        qry = "SELECT itemID FROM ItemOwner NATURAL JOIN ItemInfo WHERE ownerID = %s;" % self.ID
        self.cursor.execute(qry)
        self.items = []

        allitem = self.cursor.fetchall()
        for item in allitem:
            self.items.append(Item(cnx=self.cnx, cursor=self.cursor,itemID=item[0]))
        return self.items

    def getComplaints(self):
        '''
        :return: self.compliants
            self.compliants: list of dict{itemID,description,compliantTime }
        '''
        qry =("SELECT itemID, description, compliantTime FROM Complaint NATURAL JOIN ItemOwner "
              "WHERE justified = TRUE AND ownerID = %s;"% self.ID)
        self.cursor.execute(qry)
        self.compliants = []
        for compliant in self.cursor:
            self.compliants.append({'itemID':compliant[0], 'description': compliant[1],
                                    'compliantTime': compliant[2].strftime("%m/%d/%Y")})
            print(self.ID, self.name, compliant[0])
        return self.compliants


    ####################### Check and update OU status #####################################
    def vipCheck(self):
        '''
        :return: check for vip status
            1. update average rating
            2. check rating and warning for update status
            3. set self.depromote = True if depromote
                   self.promote = True if promote
        '''
        # Get status, moneySpend
        self.cursor.execute("SELECT status, moneySpend FROM OUstatus WHERE ouID = %s;" % self.ID)
        info = self.cursor.fetchone()

        status, moneySpend = info[0], info[1]

        # Get Rating
        qry = ("SELECT raterID,rating FROM ItemRate NATURAL JOIN ItemOwner "
               "WHERE ownerID = %s ORDER BY postTime DESC ;" % self.ID)
        self.cursor.execute(qry)

        i, sumRate = 0,0
        rater = []
        for raterID,rating in self.cursor:
            sumRate += rating   # Get sum rate
            i += 1
            try:                # check distinct rater
                rater.index(raterID)
            except ValueError:
                rater.append(raterID)

        avgRate = 0
        if i != 0:
            avgRate = sumRate/i

            self.cursor.execute("UPDATE OUstatus SET aveRate = %s WHERE ouID = %s;" % (avgRate,self.ID))
            self.cnx.commit()

        # Check warning
        self.cursor.execute("SELECT EXISTS(SELECT * FROM Warning WHERE ouID = %s);" % self.ID)
        warn = self.cursor.fetchone()[0]

        promote = not warn and status == 0
        rateP = len(rater) >= 3 and avgRate >= 4

        # depromote to ordinary
        if avgRate < 4 and avgRate != 0 and status == 1:
            self.cursor.execute("UPDATE OUstatus SET status = 0 WHERE ouID = %s;" % self.ID)
            self.cnx.commit()
            self.depromote = True

        # promote a VIP
        elif (rateP or moneySpend>500) and promote:
            self.cursor.execute("UPDATE OUstatus SET status = 1 WHERE ouID = %s;" % self.ID)
            self.cnx.commit()
            self.promote = True

    def biddingCheck(self):
        """
        :return: check if any bid item is ready to be sold
        """
        qry =("SELECT itemID, endDay "
               "FROM BidRecord "
               "NATURAL JOIN ItemBid "
               "WHERE bidderID = %s ORDER BY bidTime DESC;" % self.ID)
        self.cursor.execute(qry)
        for hist in self.cursor:
            if (hist[1] <= datetime.datetime.now()):
                self.purchaseBidding(hist[0])
                self.cursor.execute("DELETE FROM BidRecord WHERE itemID = %s;"%hist[0])
                self.cnx.commit()


    # def compliantCheck(self):
    #     '''
    #     :return: check 2 justified compliants, if true add to warning DB
    #     '''
    #     qry = ("SELECT count(*) FROM Warning WHERE warningID = 1 AND ouID = %s;" % self.ID)
    #     self.cursor.execute(qry)
    #     count = self.cursor.fetchone()[0]
    #
    #     #  check if warn not exist
    #     if count == 0:
    #         qry =("SELECT count(*) FROM Complaint NATURAL JOIN ItemOwner JOIN OUstatus ON ownerID = ouID "
    #               "WHERE justified = TRUE AND ownerID = %s AND compliantTime > statusTime;" % self.ID)
    #         self.cursor.execute(qry)
    #         count = self.cursor.fetchone()[0]
    #         des = "Received %d Complain" % count
    #         if count >= 2:
    #             qry = ("INSERT INTO Warning(ouID, warningID, description) VALUES (%s, 1, '%s');" % (self.ID,des))
    #             self.cursor.execute(qry)
    #             self.cnx.commit()

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
        self.friendIDs=[]
        qry = ("SELECT friendID,discount,username FROM FriendList JOIN User ON friendID=ID WHERE ownerID = %s;") %self.ID
        self.cursor.execute(qry)
        for info in self.cursor:
            self.friendIDs.append(info[0])
            self.friends.append({"friendID": info[0],"discount": int(info[1]*100),"username": info[2]})
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

        try:
            if friendID in self.friendIDs:  # check if already add friend
                qry = "UPDATE FriendList SET discount = %s WHERE ownerID = %s AND friendID = %s;"
                self.cursor.execute(qry, (discount, self.ID, friendID))
                self.cnx.commit()


            else:
                qry = "INSERT INTO FriendList(ownerID, friendID, discount) VALUES (%s,%s,%s);"
                self.cursor.execute(qry, (self.ID, friendID,discount))
                self.cnx.commit()
            return True
        except mysql.connector.errors as ERR:
            print("Error in add Friend %s" % ERR)
            return False

    def getFriendRequest(self):
        self.friendReq=[]
        qry = ("SELECT ownerID,username FROM FriendList JOIN User ON ownerID=ID WHERE friendID = %s;") %self.ID
        self.cursor.execute(qry)
        for info in self.cursor:
            if info[0] not in self.friendIDs:
                self.friendReq.append({"friendID": info[0],"username": info[1]})
        return self.friendReq

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

            return iID
        except mysql.connector.errors as ERR:
            print(ERR)
            return False

    def insertView(self, itemID):
        qry = "INSERT INTO ItemView(itemID) VALUE (%s);" % int(itemID)
        self.cursor.execute(qry)
        self.cnx.commit()

    def submitBiddingItem(self,image, title, description, usedStatus, startPrice, endDay):
        try:
            itemID = self.submitItem()
            qry = ("INSERT INTO ItemInfo(itemID, image, title, description, priceType) "
                   "VALUE (%s,%s,%s,%s,%s);")
            self.cursor.execute(qry,(int(itemID),image,title,description,True))
            self.cnx.commit()


            self.insertView(itemID)

            endDay = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=endDay),
                                                     datetime.time(23, 59,59))
            qry = "INSERT INTO ItemBid(itemID, startPrice,usedStatus,endDay) VALUE (%s,%s,%s,%s);"
            self.cursor.execute(qry, (int(itemID), float(startPrice), usedStatus, endDay))
            self.cnx.commit()
            return True
        except Exception as ERR:
            print('submit failded by error : %s' %ERR)
            return False

    def submitFixedPriceItem(self,image, title, description, price,available):
        try:
            itemID = self.submitItem()
            qry = ("INSERT INTO ItemInfo(itemID, image, title, description, priceType) "
                   "VALUE (%s,%s,%s,%s,%s);")
            self.cursor.execute(qry, (int(itemID),image,title,description,False))
            self.cnx.commit()

            self.insertView(itemID)

            qry = "INSERT INTO FixedPrice(itemID, price,availableNum) VALUE (%s,%s,%s);"
            self.cursor.execute(qry , (int(itemID), float(price), int(available)))
            self.cnx.commit()
            return True
        except Exception as ERR:
            print('submit failded by error : %s' % ERR)
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
        try:
            return self.cursor.fetchone()[0]
        except TypeError:
            return 0



    def calculatePurchase(self, itemID, price, numWant=1):
        """
        :param itemID: item want to purchase
        :return: list of [basePrice, taxAmount, deductFriend,deductVIP,finalPrice]
        """
        basePrice = price*numWant

        friendDiscount =  self.checkFriendDiscount(itemID)
        vipDiscount = 0.05 if self.status == 1 else 0

        deductF = round(basePrice * friendDiscount,2)
        deductV = round(basePrice * vipDiscount,2)
        taxAmount = round(basePrice * self.taxRate,2)
        finalPrice = basePrice + taxAmount - deductF - deductV

        return [basePrice, taxAmount, deductF,deductV,finalPrice]



    def bidding(self,itemID, price):
        # record bidding in BidRecord
        # bidderID = self.ID
        qry = ("SELECT EXISTS(SELECT * FROM BidRecord WHERE itemID = %s AND bidderID = %s );" % (itemID, self.ID))
        self.cursor.execute(qry)
        if not self.cursor.fetchone()[0]:
            qry = ("INSERT INTO BidRecord(itemID, bidderID, bidPrice) VALUES (%s,%s,%s);" %(itemID,self.ID,price))
            self.cursor.execute(qry)
            self.cnx.commit()
            return True
        return False


    def purchaseFixedPrice(self, itemID, singlePrice, numBuy,numLeft):
        """
        :param itemID(int):  itemID of item want to buy
        :param singlePrice(float):  price of the item
        :param numBuy(int): number of item want to but
        :param numLeft(int): number of item left after purchase
        :return:
            - True if update in DB; add to transaction, change availableNum in FixedPrice, check saleStatus in ItemInfo
            - False if duplicate purchase
        """
        try:
            finalPrice = self.calculatePurchase(itemID=itemID, price=singlePrice, numWant=numBuy)[-1]
            qry = ("INSERT INTO Transaction(itemID, buyerID, singlePrice, priceTotal,numDeal) "
                   "VALUES (%s,%s,%s,%s,%s)" % (itemID,self.ID, singlePrice,finalPrice,numBuy))
            self.cursor.execute(qry)

            qry = ("UPDATE FixedPrice SET availableNum = %s WHERE itemID = %s;"%(numLeft,itemID))
            self.cursor.execute(qry)

            if numLeft == 0:
                qry = ("UPDATE ItemInfo SET saleStatus = FALSE WHERE itemID = %s;" % itemID)
                self.cursor.execute(qry)

            self.cnx.commit()
            return True
        except mysql.connector.errors.IntegrityError:
            return False

    def purchaseBidding(self, itemID):
        '''
        :param itemID: bidding item id
        :return:
            assign second highest bidder to purchase the item, update transaction
            delete all bid recod for this item
        '''
        item = Item(cnx=self.cnx,cursor=self.cursor,itemID=itemID)

        finalPrice = self.calculatePurchase(itemID=itemID, price=item.secondPrice)[-1]

        qry = ("INSERT INTO Transaction(itemID, buyerID, singlePrice, priceTotal) VALUES (%s,%s,%s,%s);"
               %(itemID,item.secondBidder,item.secondPrice,finalPrice))
        self.cursor.execute(qry)

        self.cursor.execute("DELETE FROM BidRecord WHERE itemID = %s;"% itemID)
        self.cnx.commit()

    ####################### Transactions (VIEW/ACCEPT/DECLINE) #####################################
    def getBidRecord(self):
        self.bidHist = []
        qry =("SELECT itemID, title, ownerID,username,bidPrice,bidTime, endDay "
               "FROM BidRecord NATURAL JOIN ItemInfo "
               "NATURAL JOIN ItemBid NATURAL JOIN ItemOwner "
               "JOIN User ON ownerID = ID "
               "WHERE bidderID = %s ORDER BY bidTime DESC;" % self.ID)
        self.cursor.execute(qry)

        for hist in self.cursor:
            self.bidHist.append({'itemID':hist[0],'itemTitle': hist[1], 'sellerID': hist[2],
                                 'sellerName': hist[3],'bidPrice': round(hist[4],2),'bidTime': hist[5].strftime("%m/%d/%Y, %H:%M"),
                                 'endTime': hist[6].strftime("%m/%d/%Y, %H:%M")})
        return self.bidHist


    def getBuyHistory(self):
        """
        :param ouID: the buyer ID
        :return: list of dict in form:
                {'itemID'(int), 'itemTitle'(str), 'sellerID'(int), 'sellerName'(str),'price'(float),'time'(str),'ship'(bool) }
        """

        self.buyHist = []
        qry = ("SELECT title, ownerID,username,priceTotal,dealTime,shippingStatus,itemID, "
               "(SELECT EXISTS(SELECT * FROM Complaint WHERE itemID = ItemInfo.itemID AND complainerID = %s)), "
               "(SELECT EXISTS(SELECT * FROM ItemRate WHERE itemID = ItemInfo.itemID AND raterID = %s))"
               "FROM Transaction NATURAL JOIN ItemOwner "
               "NATURAL JOIN ItemInfo "
               "JOIN User ON ownerID = ID "
               "WHERE buyerID = %s ORDER BY dealTime DESC;" % (self.ID,self.ID,self.ID))

        self.cursor.execute(qry)

        for hist in self.cursor:
            self.buyHist.append({'itemID':hist[6],'itemTitle': hist[0], 'sellerID': hist[1],
                                 'sellerName': hist[2],'price': round(hist[3],2),'time': hist[4].strftime("%m/%d/%Y"),
                                 'ship': hist[5], 'complained': hist[7],'rated': hist[8]})
        return self.buyHist

    def getSaleHistory(self):
        """
        :param ouID: seller ID
        :return: list of dict in form:
                {'itemID'(int),'itemTitle'(str), 'buyerID'(int), 'buyerName'(str),'price'(float),'time'(str),'ship'(bool) }
        """
        self.saleHist = []
        qry = ("SELECT title, buyerID,username,priceTotal,dealTime,shippingStatus,itemID "
               "FROM Transaction NATURAL JOIN ItemOwner "
               "NATURAL JOIN ItemInfo "
               "JOIN User ON buyerID = ID "
               "WHERE ownerID = %s ORDER BY dealTime DESC;" % self.ID)

        self.cursor.execute(qry)
        for hist in self.cursor:
            self.saleHist.append({'itemID':hist[6],'itemTitle': hist[0], 'buyerID': hist[1],
                                 'buyerName': hist[2], 'price': round(hist[3],2), 'time': hist[4].strftime("%m/%d/%Y"),
                                 'ship': hist[5]})

        return self.saleHist


    def acceptSale(self,itemID, buyerID, price):
        # Charge money from buyer
        qry = ("UPDATE OUstatus SET moneySpend = moneySpend + %s WHERE ouID = %s;" %(price,buyerID))
        self.cursor.execute(qry)
        #  need check VIP Status in general

        # Change ship status
        qry = ("UPDATE Transaction SET shippingStatus = true "
               "WHERE itemID = %s AND buyerID = %s;" % (itemID,buyerID))

        self.cursor.execute(qry)
        self.cnx.commit()


    def declineSale(self,itemID, buyerID):
        # delete transaction
        qry = ("DELETE FROM Transaction WHERE itemID = %s AND buyerID = %s;" % (itemID,buyerID))
        self.cursor.execute(qry)

        # Add warning
        description = 'Decline Sale of Item %d for Buyer %d' % (itemID,buyerID)
        qry = ("INSERT INTO Warning(ouID, warningID, description)  VALUES (%s,%s,'%s');"
               % (self.ID, 2,description))
        self.cursor.execute(qry)

        self.cnx.commit()

    ####################### Transactions (VIEW/ACCEPT/DECLINE) #####################################
    def submitRating(self,itemID, rating,description):
        # add rating to DB
        # check for bad rating that will cause warning or depromotion
        # check for good rating that will cause promotion
        qry = ("INSERT INTO ItemRate(itemID, raterID, rating, description) VALUES (%s,%s,%s,'%s');"
               %(itemID,self.ID,rating,description))
        self.cursor.execute(qry)
        self.cnx.commit()

        self.ratingCheck()

    def submitCompliant(self,itemID, description):
        qry = ("INSERT INTO Complaint(itemID, complainerID, description) VALUES (%s,%s,'%s');"
               % (itemID, self.ID, description))
        self.cursor.execute(qry)
        self.cnx.commit()




    ####################### Compliant and Warning View #####################################
    # def getComplaints(self):
    #     self.cursor.execute("SELECT itemID, description, compliantTime FROM Complaint NATURAL JOIN ItemOwner WHERE ownerID = %s;"% self.ID)
    #     self.complaintList = []
    #
    #     for complaint in self.cursor:
    #         self.complaintList.append({"itemID": complaint[0],"description":complaint[1],
    #                                   "compliantTime":complaint[2]})
    #     return self.complaintList

    def getWarnings(self):
        self.cursor.execute("SELECT warningID, description, warnTime FROM Warning WHERE ouID = %s;" % self.ID)
        self.warningList = []

        for warning in self.cursor:
            self.warningList.append({'warningID': warning[0], 'description':warning[1],
                                      'warnTime':warning[2].strftime("%m/%d/%Y")})
        return self.warningList



    ########################## Check Rating #####################################

    def ratingCheck(self):
        # Get Rating
        qry = ("SELECT rating FROM ItemRate NATURAL JOIN ItemOwner "
               "WHERE raterID = %s ORDER BY postTime DESC ;" % self.ID)
        self.cursor.execute(qry)

        lowRating, highRating = 0, 0
        for rating in self.cursor:

            if rating[0] <= 1:
                lowRating +=1
                highRating = 0
            elif 2<= rating[0] <5:
                lowRating, highRating = 0, 0
            elif rating[0] == 5:
                lowRating = 0
                highRating += 1

            if lowRating >= 3 or highRating >= 3:
                des = "Give Too Many High Rating" if highRating >= 3 else "Give Too Many Low Rating"
                qry = ("REPLACE INTO Warning(ouID, warningID, description) VALUES (%s, 0, '%s');" % (self.ID,des))
                self.cursor.execute(qry)
                self.cnx.commit()



    def addWarning(self,warningID, description):
        qry = "INSERT INTO Warning(ouID, warningID, description) VALUES (%s,%s,'%s');"%(self.ID,warningID,description)
        self.cursor.execute(qry)
        self.cnx.commit()







