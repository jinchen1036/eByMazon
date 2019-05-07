import mysql.connector
from kivy.core.image import Image as CoreImage
from io import BytesIO

class Item():
    def __init__(self,cnx,cursor, itemID):
        self.cnx = cnx
        self.cursor = cursor
        self.itemID = itemID
        self.itemProfile()


    def itemProfile(self):
        """
        :return: Get all information of the item
        """
        # return image, title, priceType, saleStatus, postTime
        # need for view item action

        qry = "SELECT image, title, description, priceType,likeness,dislike,saleStatus, approvalStatus FROM ItemInfo WHERE itemID = %s;"%self.itemID
        self.cursor.execute(qry)
        profile = self.cursor.fetchone()

        self.title, self.descrpition, self.priceType = profile[1],profile[2],profile[3]
        self.likeness,self.dislike = profile[4],profile[5]
        self.saleStatus, self.approvalStatus = profile[6], profile[7]
        self.image = CoreImage(BytesIO(profile[0]), ext="png").texture

        qry = "SELECT ownerID from ItemOwner WHERE itemID = %s;"% self.itemID
        self.cursor.execute(qry)
        self.owner = self.cursor.fetchone()[0]


        qry = "SELECT frequency from ItemView WHERE itemID = %s;"% self.itemID
        self.cursor.execute(qry)
        self.views = self.cursor.fetchone()[0]

        self.rating = 0

        if self.priceType:      # for bidding
            self.getBiddingInfo()
            self.getBiddings()
        else:                   # for fixed
            self.getFixedinfo()
            self.getRating()

    def getFixedinfo(self):
        qry = "SELECT price, availableNum FROM FixedPrice WHERE itemID = %s;"%self.itemID
        self.cursor.execute(qry)
        info = self.cursor.fetchone()
        if info:
            self.price,self.available = info[0],info[1]

    def getBiddingInfo(self):
        qry = "SELECT startPrice, usedStatus,endDay FROM ItemBid WHERE itemID = %s;"%self.itemID

        self.cursor.execute(qry)
        info = self.cursor.fetchone()
        if info:
            self.price, self.endDay = info[0], "{:%b %d, %Y}".format(info[2])
            self.usedStatus = "True" if info[1] else "False"

    def getBiddings(self):
        qry = "SELECT bidderID, bidPrice,bidTime FROM BidRecord WHERE itemID = %s ORDER BY bidPrice DESC;"%self.itemID
        self.cursor.execute(qry)

        b1 = self.cursor.fetchone()
        if b1:
            self.highestBidder = b1[0]
            self.highestPrice = b1[1]
            self.highestTime = b1[2]
            b2 = self.cursor.fetchone()
            if b2:
                self.secondBidder = b2[0]
                self.secondPrice = b2[1]
                self.secondTime = b2[2]



    def checkLiked(self,ouID):
        qry = "SELECT EXISTS(SELECT * from ItemOwner WHERE itemID=%s AND ownerID =%s);" % (self.itemID,ouID)
        self.cursor.execute(qry)

        if self.cursor.fetchone()[0]:
            return False

        qry = "SELECT EXISTS(SELECT * from ItemLike WHERE itemID=%s AND ouID =%s);" % (self.itemID,ouID)
        self.cursor.execute(qry)
        if self.cursor.fetchone()[0]:
            return False
        return True

    def addLiked(self,ouID):
        qry = "INSERT INTO ItemLike(itemID,ouID) VALUES (%s,%s);" %  (self.itemID,ouID)
        self.cursor.execute(qry)
        # self.cnx.commit()

    def likeItem(self,ouID):
        if self.checkLiked(ouID):
            qry = "UPDATE ItemInfo SET likeness = likeness+1 WHERE itemID = %s;" % self.itemID
            try:
                self.cursor.execute(qry)
                self.likeness+=1
                self.addLiked(ouID)
                self.cnx.commit()

            except mysql.connector.errors as err:
                print("Update likeness error: %s"%err)

    def dislikeItem(self,ouID):
        if self.checkLiked(ouID):
            qry = "UPDATE ItemInfo SET dislike = dislike+1 WHERE itemID = %s;"% self.itemID
            try:
                self.cursor.execute(qry)
                self.dislike+=1
                self.addLiked(ouID)
                self.cnx.commit()
            except mysql.connector.errors as err:
                print("Update dislike error: %s"%err)


    def addView(self):
        qry = "UPDATE ItemView SET frequency = frequency+1 WHERE itemID = %s;"% self.itemID
        try:
            self.cursor.execute(qry)
            self.views +=1
            self.cnx.commit()
        except mysql.connector.errors as err:
            print("Update views error: %s"%err)

    def getRating(self):
        qry = ("SELECT username, rating, description FROM itemRate "
               "JOIN User ON ItemRate.raterID = User.ID WHERE itemID = %s ORDER BY postTime DESC;") % self.itemID
        self.cursor.execute(qry)
        self.rating = 0
        self.ratings = []

        i = 0
        for info in self.cursor:
            self.rating += int(info[1])
            i+=1
            self.ratings.append({"rater":info[0],"rating": info[1],"comment": info[2]})

        if i > 0:
            self.rating /= i
        return self.ratings