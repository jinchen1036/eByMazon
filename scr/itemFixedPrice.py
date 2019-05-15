from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty,NumericProperty

try:
    from scr.GlobalVariable import globalV
    from scr.Item import Item
except ModuleNotFoundError:
    from GlobalVariable import globalV
    from Item import Item

class fixedItem(Screen):
    itemIndex = NumericProperty()
    user = BooleanProperty()
    itemID = NumericProperty()

    def tohome(self):
        self.warn = False
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].clear()
        self.ids["purchase"].ids["purchaseManager"].current = "empty"
        globalV.root.tohome()

    def initInfo(self,index, refresh = False):
        if refresh:
            item = Item(itemID=self.itemID, cursor=globalV.cursor,cnx= globalV.cnx)
        else:
            item = globalV.itemList[index]
            item.addView()
        self.purchased = False
        self.itemID = item.itemID
        self.itemIndex = index
        self.price= item.price
        self.numberAva = item.available
        self.user = not globalV.root.login
        self.ids['itemImage'].texture = item.image
        self.ids['itemTitle'].text = item.title
        self.ids['itemDescription'].text=item.descrpition
        self.ids['itemRates'].text = str(item.rating) if item.rating else "None"
        self.ids['itemPrice'].text="$"+str(item.price)
        self.ids['itemAvailable'].text = str(item.available)
        self.ids['itemLike'].text = str(item.likeness)
        self.ids['itemDislike'].text = str(item.dislike)
        self.ids['itemRate'].data = item.getRating()
        self.disableAction = globalV.root.checkDisable(item.itemID)



    def dislikeItem(self,name):
        globalV.root.dislikeItem(name,self.itemIndex)

    def likeItem(self,name):
        globalV.root.likeItem(name,self.itemIndex)

    def purchasing(self):
        # purchase Item
        if self.purchased:
            item = globalV.itemList[self.itemIndex]
            numwant = int(self.ids['purchaseInfo'].text)
            numLeft = self.numberAva - numwant
            purchase = globalV.ou.purchaseFixedPrice(item.itemID, item.price,numwant,numLeft)
            self.purchased = False
            if purchase:
                self.ids["purchase"].ids["purchaseManager"].current = "empty"
                self.initInfo(self.itemIndex,refresh=True)
            else:
                self.ids["purchase"].ids["purchaseManager"].current = "duplicate"

    def cancelPurchase(self):
        if self.purchased:
            self.purchased = False
            self.ids["purchaseInfo"].text = ""
            self.ids["purchase"].ids["purchaseManager"].current = "cancel"


    def checkNumwant(self,num):
        try:
            int(num)
            if int(num) <= self.numberAva:
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
            numWant = int(self.ids["purchaseInfo"].text)
            purchaseInfo = [item.price,numWant ]
            purchaseInfo.extend(globalV.ou.calculatePurchase(item.itemID,item.price,numWant))

            self.purchased = True
            self.ids["purchase"].infoLoad(purchaseInfo)
            self.ids["purchase"].ids["purchaseManager"].current = "Purchase"