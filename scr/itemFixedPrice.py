from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty,NumericProperty

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV

class fixedItem(Screen):
    itemIndex = NumericProperty()
    user = BooleanProperty()

    def tohome(self):
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].clear()
        self.ids["purchase"].ids["purchaseManager"].current = "empty"
        globalV.root.tohome()

    def initInfo(self,index):
        item = globalV.itemList[index]
        item.addView()
        self.itemIndex = index
        self.user = not globalV.root.login
        self.ids['itemImage'].texture = item.image
        self.ids['itemTitle'].text = item.title
        self.ids['itemDescription'].text=item.descrpition
        self.ids['itemPrice'].text="$"+str(item.price)
        self.ids['itemAvailable'].text = str(item.available)
        self.ids['itemLike'].text = str(item.likeness)
        self.ids['itemDislike'].text = str(item.dislike)
        self.disableAction = globalV.root.checkDisable(item.itemID)


    def dislikeItem(self,name):
        globalV.root.dislikeItem(name,self.itemIndex)

    def likeItem(self,name):
        globalV.root.likeItem(name,self.itemIndex)

    def purchasing(self):
        # purchase Item
        self.ids["purchase"].ids["purchaseManager"].current = "empty"

    def cancelPurchase(self):
        self.purchased = False
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].ids["purchaseManager"].current = "cancel"

    def toPurchase(self):
        item = globalV.itemList[self.itemIndex]
        numWant = int(self.ids["purchaseInfo"].text)
        purchaseInfo = [item.price,numWant ]
        purchaseInfo.extend(globalV.ou.calculatePurchase(item.itemID,item.price,numWant))

        self.purchased = True
        self.ids["purchase"].infoLoad(purchaseInfo)
        self.ids["purchase"].ids["purchaseManager"].current = "Purchase"