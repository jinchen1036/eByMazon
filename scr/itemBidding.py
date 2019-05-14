from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty,NumericProperty

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV

class biddingItem(Screen):
    itemIndex = NumericProperty()
    user = BooleanProperty()
    def tohome(self):
        self.warn = False
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].clear()
        self.ids["purchase"].ids["purchaseManager"].current = "empty"
        globalV.root.tohome()

    def initInfo(self,index):
        item = globalV.itemList[index]
        item.addView()
        self.bid = False
        self.itemIndex = index
        self.itemID = item.itemID
        self.price = item.price
        self.user = not globalV.root.login
        self.ids['itemImage'].texture = item.image
        self.ids['itemTitle'].text = item.title
        self.ids['itemDescription'].text=item.descrpition
        self.ids['itemPrice'].text="$"+str(item.price)
        self.ids['itemLike'].text = str(item.likeness)
        self.ids['itemDislike'].text = str(item.dislike)
        self.ids['itemUsed'].text = str(item.usedStatus)
        self.disableAction = globalV.root.checkDisable(item.itemID)

        try:
            self.ids['itemBid'].text = "$" + str(item.highestPrice)
        except AttributeError:
            self.ids['itemBid'].text = "None"




    def dislikeItem(self,name):
        globalV.root.dislikeItem(name,self.itemIndex)
    def likeItem(self,name):
        globalV.root.likeItem(name,self.itemIndex)

    def bidding(self):
        # purchase Item
        bid = globalV.ou.bidding(self.itemID,float(self.ids["purchaseInfo"].text) )
        self.bid = False
        if bid:
            self.ids["purchase"].ids["purchaseManager"].current = "empty"
        else:
            self.ids["purchase"].ids["purchaseManager"].current = "bidWarn"

    def cancelbid(self):
        self.bid = False
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].ids["purchaseManager"].current = "cancel"

    def checkNumwant(self,num):
        try:
            if float(num) >= self.price:
                self.warn = False
                return True
            self.warn = True
            return False
        except ValueError:
            self.warn = True
            return False


    def toPurchase(self):
        check = self.checkNumwant(self.ids["purchaseInfo"].text)
        if check:
            item = globalV.itemList[self.itemIndex]
            # numWant = 1
            bidprice = float(self.ids["purchaseInfo"].text)
            purchaseInfo = [bidprice, 1]
            purchaseInfo.extend(globalV.ou.calculatePurchase(item.itemID,bidprice,1))

            self.bid = True
            self.ids["purchase"].infoLoad(purchaseInfo)
            self.ids["purchase"].ids["purchaseManager"].current = "Purchase"