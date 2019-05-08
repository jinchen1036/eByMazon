import os
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV

######################################### OU Item Page ###############################################
class LoadImage(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ouItem(Screen):
    def backProfile(self):
        globalV.root.toProfile()

    def backPostItemPage(self):
        self.getOUitem()
        self.ids["ouItemManager"].current = "itemHome"
        self.clearBidItemInput()
        self.clearFixedItemInput()

    ################### Clear FUNCTIONS ################
    def clearBidItemInput(self):
        self.ids['itemTitle'].text = ""
        self.ids['itemDescription'].text = ""
        self.ids['itemPrice'].text = ""
        self.ids['itemBidDay'].text = ""
        self.ids['image'].text = "Choose Image"
        self.ids['bidItemWarning'].text = ""
        self.ids['new'].active = False
        self.ids['used'].active = False
        self.image = ""

    def clearFixedItemInput(self):
        self.ids['itemTitle1'].text = ""
        self.ids['itemDescription1'].text = ""
        self.ids['itemPrice1'].text = ""
        self.ids['itemNumbers1'].text = ""
        self.ids['fixedItemWarning'].text = ""
        self.image = ""
        # self.isTitle, self.isDescription, self.isPrice, self.isNumber = True, True, True, True

    ############ Getting image ########################
    def getImage(self):
        content = LoadImage(load=self.loadImage, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def loadImage(self,path, filename):
        with open(os.path.join(path, filename[0]),'rb') as file:
            self.image = file.read()
        filename= str(filename[0])
        filename = filename.split('/')
        self.ids['image'].text = filename[-1]
        self.ids['image1'].text = filename[-1]
        self._popup.dismiss()
    def dismiss_popup(self):
        self._popup.dismiss()

    ################### Display all Items ################
    def getOUitem(self):
        ouItems = globalV.ou.getItem()
        waitI = []
        fixedI = []
        bidI = []
        for item in ouItems:
            typeStr = "Bidding" if item.priceType else "Fixed Price"
            if not item.approvalStatus:
                waitI.append({"image": item.image,"title": item.title, "priceType": item.priceType,
                              "price": str(item.price), "typeStr": typeStr, "description": item.descrpition})
            else:
                # sale = "Sold" if item.saleStatus else "On Sale"
                try:
                    highestPrice = str(item.highestPrice)
                except AttributeError:
                    highestPrice = "None"

                saleStatus = False
                if item.saleStatus:
                    saleStatus = True
                if item.priceType:
                    bidI.append({"image": item.image, "title": item.title,"price": str(item.price),
                                 "currentBid": highestPrice, "typeStr": typeStr,
                                 "description": item.descrpition, "reviews": str(item.views),
                                 "likes": str(item.likeness), "dislike": str(item.dislike), "status": saleStatus})

                else:
                    fixedI.append({"image": item.image, "title": item.title,"price": str(item.price),
                                 "numLeft": str(item.available), "typeStr": typeStr,
                                 "description": item.descrpition, "reviews": str(item.views),
                                 "likes": str(item.likeness), "dislike": str(item.dislike), "status": saleStatus})

        self.ids["waitItem"].data = waitI
        self.ids["itemFixed"].data = fixedI
        self.ids["itemBid"].data = bidI

    ################### Submit FUNCTIONS ################
    def updateStatus(self, status):
        self.isUsed = status

    def submitBidingItem(self, title, description, itemPrice, itemBidDay):
        found1 = globalV.root.change_to_star(title)
        found2 = globalV.root.change_to_star(description)
        if found1 or found2:
            result=''
            result = [x for x in [found1,found2] if x!=False]
            print(result)
            pop = ''
            for word in result:
                pop+= word + ' '
            print(pop)
            globalV.root.tobaooPoo(pop)
            if found1: 
                self.ids['itemTitle'].text = found1
            if found2: 
                self.ids['itemDescription'].text = found2
            
        if not(globalV.general.checkEmpty(title) or globalV.general.checkEmpty(description) or globalV.general.checkFloat(itemPrice) or globalV.general.checkInt(itemBidDay)):
            condition = False
        else:
            try:
                image = self.image
                condition = True
                if image == "":
                    condition = False
            except AttributeError as err:
                print(err)
                condition = False

        if not condition or not (self.ids['new'].active or self.ids['used'].active):
            self.ids['bidItemWarning'].text = "Fail to Submit!!! Input should not be empty\
            \nStart Price should be an number (integer or decimal), one checkbox should be checked.\
            \nBid Day should be integer, for how many days you want bidding last."

        else:
            self.ids['bidItemWarning'].text = ""
            globalV.ou.submitBiddingItem(image=self.image,title=title,description=description,
                                 usedStatus=self.isUsed,startPrice=float(itemPrice),endDay=int(itemBidDay))
            print("submitted")
            self.clearBidItemInput()
            self.backPostItemPage()

    def submitFixedItem(self, title, description, itemPrice, number_available):
        found1 = globalV.root.change_to_star(title)
        found2 = globalV.root.change_to_star(description)
        if found1 or found2:
            result=''
            result = [x for x in [found1,found2] if x!=False]
            print(result)
            pop = ''
            for word in result:
                pop+= word + ' '
            print(pop)
            globalV.root.tobaooPoo(pop)
            if found1: 
                self.ids['itemTitle1'].text = found1
            if found2: 
                self.ids['itemDescription1'].text = found2

        if not(globalV.general.checkEmpty(title) or globalV.general.checkEmpty(description) or globalV.general.checkFloat(itemPrice) or globalV.general.checkInt(number_available)):
            condition = False
        else:
            try:
                image = self.image
                condition = True
                if image == "":
                    condition = False
            except AttributeError as err:
                print(err)
                condition = False

        if not condition:
            self.ids['fixedItemWarning'].text = "Fail to Submit!!!\nInput should not be Empty!\
            \nPrice should be integer or decimal.\
            \nNumber available should be integer."
        else:
            self.ids['fixedItemWarning'].text = ""
            globalV.ou.submitFixedPriceItem(image=self.image, title=title, description=description,
                                    price=float(itemPrice), available=int(number_available))

            print("submitted")
            self.clearFixedItemInput()
            self.backPostItemPage()