# kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty,ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

######### import self define classes #################
try:
    from scr.GU import GU
    from scr.SU import SU
    from scr.OU import OU
    from scr.Item import Item
    from scr.GeneralFunctions import General
    from scr.GlobalVariable import globalV

    # KV page function
    from scr.Login import appealPop,Login
    from scr.Signup import Signup, editProfile

    from scr.itemFixedPrice import fixedItem
    from scr.itemBidding import biddingItem
    from scr.itemPurchase import FixedPurchase,BidPurchase

    from scr.ouHome import ouInformation,ouInfo,ouWarning
    from scr.ouItem import ouItem,LoadImage
    from scr.ouFriend import friendInfo,friendList,friendRequest
    from scr.ouTransaction import transactionHistory,bought

    from scr.suManagement import guApplications,GUapplication,suItemPost,suItemSale,blackTaboo
    from scr.suManagement import complainInfo,processCompliant, itemManage

    from scr.Taboo import tabooPop

except ModuleNotFoundError:
    from GU import GU
    from SU import SU
    from OU import OU
    from Item import Item
    from GeneralFunctions import General
    from GlobalVariable import globalV

    # KV page function
    from Login import appealPop,Login
    from Signup import Signup

    from itemFixedPrice import fixedItem
    from itemBidding import biddingItem
    from itemPurchase import FixedPurchase,BidPurchase

    from ouHome import ouInformation,ouInfo,ouWarning
    from ouItem import ouItem,LoadImage
    from ouFriend import friendInfo,friendList
    from ouTransaction import transactionHistory,bought

    from suManagement import guApplications,GUapplication,suItemPost,suItemSale,blackTaboo
    from suManagement import complainInfo, processCompliant, itemManage
    from Taboo import tabooPop
    # from notificationPop import notificationPop

################################## Home Page Item Recycle View ###############################################
class item(BoxLayout):
    # the item frame in homepage, implemented in feature.kv
    def getItem(self):
        if self.priceType:
            globalV.root.tobidItem(self.itemIndex)
        else:
            globalV.root.tofixedItem(self.itemIndex)

class suTransaction(Screen):
    def tohome(self):
        globalV.root.ids['screenmanager'].current = "suHomepage"
    def Transactions(self):
        self.ids['transactions'].data = globalV.su.getTransaction() #data selection to be fixed
                                                            #connections done

class editPassword(FloatLayout):
    back = ObjectProperty(None)
    submit = ObjectProperty(None)


####################### Main Class #############################
class Manager(Screen):
    login = BooleanProperty()
    ouID = ObjectProperty()
    sort = 1
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.displayItem()          # Display Item

    ####################### Display/Search/Sort Homepage Item #############################
    def clearHome(self):
        self.ids['found'].text = ""
        self.ids['search_id'].text =""
    def displayItem(self):
        globalV.itemList = globalV.general.popularItem()
        self.itemShow()

    def displayOULikeItem(self):
        globalV.itemList = globalV.general.ouPopularItem(globalV.ou.ID)
        self.itemShow()

    def searchKeyword(self, word):
        self.ids['found'].text = ""
        if word == "":
            self.displayItem()
        else:
            globalV.itemList = globalV.general.searchItem(word)

            if globalV.ou is not None:
                globalV.ou.searchAdd(word)

            if globalV.itemList:
                self.sortItem(self.sort)
                self.ids['found'].text = ""
            else:
                self.ids['homeItem'].data = []
                self.ids['found'].text = "No result found for %s" % word
                print("No result for %s" % word)

    def sortItem(self, sortType):
        self.sort = sortType
        if sortType == 1:       # By popular views
            globalV.itemList = globalV.general.sortItem(globalV.itemList, 'views',decs=True)
        elif sortType == 2:     # By Rating
            globalV.itemList = globalV.general.sortItem(globalV.itemList, 'rating',decs=True)
        elif sortType == 3:     # By low to high price
            globalV.itemList = globalV.general.sortItem(globalV.itemList, 'price',decs=False)
        elif sortType == 4:     # By high to low price
            globalV.itemList = globalV.general.sortItem(globalV.itemList, 'price', decs=True)
        self.itemShow()

    def itemShow(self):
        returndict = []
        i = 0
        if globalV.itemList:
            for item in globalV.itemList:
                typeStr = "Bidding" if item.priceType else "Fixed Price"
                returndict.append(
                    {"itemIndex": i, "image": item.image, "title": item.title, "priceType": item.priceType,
                     "price": str(item.price), "reviews": str(item.views), "likes": str(item.likeness),
                     "typeStr": typeStr, "rating": str(item.rating)})
                i += 1
            self.ids['homeItem'].data = returndict
    ####################### Homepage Two Button #############################
    def tologin(self):
        if self.login:      # logout
            self.login = False
            globalV.ou = None
            self.clearHome()
            self.displayItem()
        else:               # login
            self.clearHome()
            self.ids['screenmanager'].current = "loginpage"

    def signProfile(self):
        if self.login:      # my account
            self.toProfile()
        else:               # sign up
            self.tosignup()

    def suLogout(self):     # logout from su homepage
        self.login = False
        globalV.su = None
        self.tohome()

    ####################### Goto OU Profile #############################

    def toProfile(self):
        status = "VIP" if globalV.ou.status else "Ordinary User"
        self.ids['ouName'].text = "Name: %s" % globalV.ou.name
        self.ids['ouPhone'].text = "Phone: %s" % globalV.ou.phone
        self.ids['ouEmail'].text = "Email: %s"% globalV.ou.email
        self.ids['ouCard'].text = "Card Number: %s"% globalV.ou.card
        self.ids['ouAddress'].text = "Address: %s"% globalV.ou.address
        self.ids['ouState'].text = "State: %s"% globalV.ou.state
        self.ids['ouRate'].text = "Current Rating: %s"% globalV.ou.avgRate
        self.ids['ouMoney'].text = "Current Money Spend: %s"% globalV.ou.moneySpend
        self.ids['ouStatus'].text = "Current Status: %s"% status
        self.ids['ouStatusTime'].text = "Status Start Time: {:%b %d, %Y}".format(globalV.ou.statusTime)
        self.ids['screenmanager'].current = "profilePage"



    ###################### Change Password and Ou Info ###################
    def getPassword(self):
        content = editPassword(back=self.dismiss_popup, submit=self.changePassword)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()
    def dismiss_popup(self):
        self._popup.dismiss()

    def changePassword(self,newpassword):
        print("Change Password %s" % newpassword)
        # Need Check inputs, add warning label
        globalV.ou.changePassword(newpassword)
        self.dismiss_popup()

    ###################### To Item Page from homepage ###################
    def checkDisable(self, itemID):
        if globalV.ou is not None:
            if globalV.general.checkOwner(globalV.ou.ID,itemID):
                return False
        return True

    def tofixedItem(self,itemIndex):
        self.ids['fixedItem'].initInfo(itemIndex)
        self.ids['screenmanager'].current = "fixedItem"

    def tobidItem(self,itemIndex):
        self.ids['biddingItem'].initInfo(itemIndex)
        self.ids['screenmanager'].current = "biddingItem"

    ############################# Like/Dislike Item ################################
    def likeItem(self,pagename,itemIndex):
        globalV.itemList[itemIndex].likeItem(globalV.ou.ID)
        self.ids[pagename].ids['itemLike'].text = str(globalV.itemList[itemIndex].likeness)

    def dislikeItem(self,pagename,itemIndex):
        globalV.itemList[itemIndex].dislikeItem(globalV.ou.ID)
        self.ids[pagename].ids['itemDislike'].text = str(globalV.itemList[itemIndex].dislike)

    ################################### Friend Page ################################
    def friendList(self):
        # print('friendlist')
        self.ids["friendPage"].initInfo()
        self.ids['screenmanager'].current = "friendPage"

    ################################### SU Item Page ################################
    def getSUitem(self):
        suItems = globalV.su.getAllItem()
        waitI = []
        saleI = []
        for item in suItems:
            typeStr = "Bidding" if item.priceType else "Fixed Price"

            if not item.approvalStatus:
                waitI.append({"itemID": item.itemID,"image": item.image,"title": item.title, "priceType": item.priceType,
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

                # if item.priceType:
                saleI.append({"itemID": item.itemID,"image": item.image, "title": item.title,"price": str(item.price),
                              "typeStr": typeStr,"description": item.descrpition, "reviews": str(item.views),
                             "likes": str(item.likeness), "dislike": str(item.dislike), "status": saleStatus})


        self.ids["itemManage"].ids["itemPost"].data = waitI
        self.ids["itemManage"].ids["itemSale"].data = saleI

    ################################### Change Page ################################
    def tohome(self):
        self.displayItem()
        self.ids['screenmanager'].current = "homepage"

    def tosignup(self):
        self.ids['signup'].clearSignup()
        self.ids['screenmanager'].current = "signupPage"

    def toEditProfile(self):
        self.ids['editProfile'].editInfo()
        self.ids['screenmanager'].current = "editPage"

    def toguApply(self):
        self.ids['guApply'].getApplications()
        self.ids['screenmanager'].current = "GUapplication"

    def toOuHistory(self):
        self.ids['history'].getTransaction()
        self.ids['screenmanager'].current = "historyPage"

    def toouInfo(self):
        self.ids['ouInfo'].getOUInformation()
        self.ids['screenmanager'].current = "ouInfo"

    def toitemManage(self):
        self.getSUitem()
        self.ids['screenmanager'].current = "itemManage"

    def toOuItem(self):
        self.ids['ouItem'].getOUitem()
        self.ids['screenmanager'].current = "ouItem"

    def toWarning(self):
        self.ids['ouWarning'].warningData()
        self.ids['screenmanager'].current = "ouWarning"

    def toCompliant(self):
        self.ids['processCompliant'].displayComplain()
        self.ids['screenmanager'].current ="processCompliant"

    def toBlacklist(self):
        self.ids['blackTaboo'].blackListData()
        self.ids['screenmanager'].current = "blackTaboo"

    def toSUtransaction(self):
        self.ids['screenmanager'].current = "suTransaction"
        self.ids['suTransaction'].Transactions()

    def toTaboo(self, label):
        taboo = tabooPop()
        taboo.changeLabel(label)
        taboo.open()

    def replaceTaboo(self,word):
        '''
            pre-condition: if input contains taboo
            params: userInput and taboo contained
            return: string with taboo replaced
        '''

        taboos = globalV.general.findtaboo(word)
        result = ""
        if not taboos:
            return False
      
        for taboo in taboos:
            taboo = taboo.lower()
            word = word.lower()
        
            result = word.replace(taboo, '*'*len(taboo))
            # self.taboochange = result
            print(taboo)
            print(result)
        return result

class eByMazonApp(App):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Builder.load_file("kvFiles/manage.kv")
        
        globalV.root = Manager()
        # globalV.root = Manager()
        return globalV.root

if __name__ == "__main__":

    globalV.general = General(cnx=globalV.cnx, cursor=globalV.cursor)
    globalV.guest = GU(cnx=globalV.cnx, cursor=globalV.cursor)

    eByMazonApp().run()