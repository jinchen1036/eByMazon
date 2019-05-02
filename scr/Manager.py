# mysql
import mysql.connector
import os
import datetime
from mysql.connector import errorcode
# kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.screenmanager import Screen #ScreenManager, FadeTransition
from kivy.properties import BooleanProperty,NumericProperty,ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window

# self define classes
try:
    from scr.GeneralFunctions import General
    from scr.GU import GU
    from scr.SU import SU
    from scr.OU import OU
    from scr.Item import Item
    from scr.itemPurchase import *
    # from scr.otherClass import *
except ModuleNotFoundError:
    from GeneralFunctions import General
    from GU import GU
    from SU import SU
    from OU import OU
    from Item import Item
    from itemPurchase import *
    # from otherClass import *


################################## Home Page Item Recycle View ###############################################
class item(BoxLayout):
    # the item frame in homepage, implemented in feature.kv
    def getItem(self):

        if self.priceType:
            root.tobidItem(self.itemIndex)
        else:
            root.tofixedItem(self.itemIndex)


################################################## Sign Up Page ###############################################
class Signup(Screen):
    # sign up page implement in signup.kv
    stateV,cardV,nameV = BooleanProperty(),BooleanProperty(),BooleanProperty()

    def tohome(self):
        root.tohome()

    def clearSignup(self):
        self.ids['GUusername'].text = ""
        self.ids['GUname'].text = ""
        self.ids['GUphone'].text = ""
        self.ids['GUemail'].text = ""
        self.ids['GUaddress'].text = ""
        self.ids['GUState'].text = ""
        self.ids['GUcard'].text = ""

        self.ids['warnApplication'].text = ""
        self.ids['warnUsername'].text = ""
        self.stateV, self.cardV, self.nameV = True, True,True

    def checkUsername(self,username):
        nameCheck = guest.checkUsername(username)
        if not nameCheck:
            self.ids['warnUsername'].text = "Username can be used"
        elif nameCheck == 1:
            self.ids['warnUsername'].text = "Username already existed in system"
        elif nameCheck == 2:
            self.ids['warnUsername'].text = "Username already existed in system"
        elif nameCheck == 3:
            self.ids['warnUsername'].text = "Username are in system blacklist!"

    def checkName(self,name):
        self.nameV = not guest.checkInput(name)

    def checkState(self,state):
        self.stateV = guest.checkState(state.upper())

    def checkCard(self,card):
        self.cardV = not guest.checkInput(card)

    def signUp(self,username, name, phone, email,address,state,card):
        self.checkName(name)
        self.checkState(state)
        self.checkCard(card)
        self.checkUsername(username)
        if guest.checkUsername(username) or not self.stateV or not self.cardV or not self.nameV:
            self.ids['warnApplication'].text = "Fail to Apply!!!"
        else:
            applied = guest.apply(username, name, email,card,address,state.upper(),phone)
            self.ids['warnApplication'].text = "Fail to Apply!!!" # for not approve application
            if applied:                                      # save on DB
                self.ids['warnApplication'].text = ""
                self.clearSignup()
                root.tohome()


######################################### Appeal Pop Up Page ###############################################
class appealPop(Popup):
    def homepage(self):
        appealPop.dismiss(self)
        root.clearLogin()
        root.tohome()

    def switchScreen(self, screenName):
        self.ids['appealManager'].current = screenName

    def removeOU(self):
        general.removeOU(username=root.ids['loginUsername'].text)
        self.homepage()

    def appeal(self,message):
        general.appeal(ouID=root.ouID,message=message)
        self.homepage()


######################################### OU Item Page ###############################################
class LoadImage(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

class ouItem(Screen):
    def backProfile(self):
        root.toProfile()

    def backPostItemPage(self):
        root.getOUitem()
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

    def updateStatus(self, status):
        self.isUsed = status

    ################### Submit FUNCTIONS ################
    def submitBidingItem(self, title, description, itemPrice, itemBidDay):
        if not(self.checkEmpty(title) or self.checkEmpty(description) or self.checkFloat(itemPrice) or self.checkInt(itemBidDay)):
            condition = False
        else:
            try:
                used = self.isUsed
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
            ou.submitBiddingItem(image=self.image,title=title,description=description,
                                 usedStatus=self.isUsed,startPrice=float(itemPrice),endDay=int(itemBidDay))
            print("submitted")
            self.clearBidItemInput()
            self.backPostItemPage()

    def submitFixedItem(self, title, description, itemPrice, number_available):
        if not(self.checkEmpty(title) or self.checkEmpty(description) or self.checkFloat(itemPrice) or self.checkInt(number_available)):
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
            ou.submitFixedPriceItem(image=self.image, title=title, description=description,
                                    price=float(itemPrice), available=int(number_available))

            print("submitted")
            self.clearFixedItemInput()
            self.backPostItemPage()

################################### GU Application ################################
class GUapplication(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"

    def getApplications(self):
        self.ids['application'].data = su.getGU()
        print("Refresh")

class guApplications(BoxLayout):
    def manageApplication(self,guUsername, action):
        su.manageApplication(guUsername, action)

################################### OU INFO ################################
class ouInformation(BoxLayout):
    def removeOU(self,ouID):
        su.removeOU(ouID)
        root.ids['ouInfo'].getOUInformation()

class ouInfo(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"

    def getOUInformation(self):
        ous = su.getOU()
        ouData = []
        for ou in ous:
            remove = True if ou.status == 3 else False
            status = 'Ordinary'
            if ou.status == 1:
                status = 'VIP'
            elif ou.status == 2:
                status = 'Suspend'
            elif ou.status == 3:
                status = 'Removed'

            ouData.append({'ouID': ou.ID, 'ouName': ou.name, 'ouPhone': ou.phone, 'ouEmail': ou.email,
                           'ouCard': ou.card, 'ouAddress': ou.address,'ouState':ou.state,
                           'ouStatus':status, 'ouRate': ou.avgRate, 'ouComplaint': len(ou.compliants),
                           'ouWarning': 0, 'remove': remove})
        self.ids['ouInformation'].data = ouData

################################################## Friend Page ###############################################

class friendInfo(GridLayout):
    def deleteFriend(self):
        # print(self.friendID)
        test = ou.deleteFriend(self.friendID)

    def getFriendMessage(self):
        root.ids["friendPage"].selectedFriend = self.username
        root.getMessage(self.friendID)
        # print(self.friendID)

class friendList(Screen):
    def backProfile(self):
        self.selectedFriend = " Unselected "
        root.toProfile()


    def displayFriend(self):
        friends = ou.getFriend()
        self.ids['friends'].data = friends
        print("Refresh")
    def checkInt(self, input):
        if input is None or input == '':
            return False
        try:
            if float(input) < 1:        # max discount
                return True
        except ValueError:
            return False
        return False
    # def checkFloat(self, input):
    #     return isinstance(float(input, float) or self.checkInt(input)
    def clearMsg(self):
        self.ids['warning'].text = ''
        self.ids['friendName'].text = ''
        self.ids['discount'].text = ''

    def addFriend(self, username, discount):
        if not guest.checkUsername(username) or not self.checkInt(discount):
            print(guest.checkUsername(username))
            print(self.checkInt(discount))
            self.ids['warning'].text = 'Please enter valid input'
        else:
            self.clearMsg()
            cursor.execute("SELECT ID FROM User WHERE username = '%s'" % username)
            friendID = cursor.fetchone()[0]
            ou.addFriend(friendID, float(discount))
            print("Add Friend")

    def addFriends(self,friendID,discount):
        ou.addFriend(friendID,discount)
    def sentMessage(self,message):
        if self.selectedFriend == " Unselected ":
            self.ids['send'].disable = True
            self.ids['warn'].text = "Please Select a Friend"
        elif self.ids['chat'].text =="":
            self.ids['send'].disable = True
            self.ids['warn'].text = "Can't send empty message"
        else:
            self.ids['send'].disable = False
            print(message)
            ou.sendFriendMessage(root.friendID,message)
            root.getMessage(root.friendID)
            self.ids['chat'].text = ""
            self.ids['warn'].text = ""

############################################## OU Warning Page #################################################
class ouWarning(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "profilePage"

    def warningData(self):
        warningTimes = ou.getWarnings()
        for time in warningTimes:
            if (time['warningID'] == 0):
                time['warningID'] = "low rating"
            elif (time['warningID'] == 1):
                time['warningID'] = "complaints"
            elif (time['warningID'] == 2):
                time['warningID'] = "decline deal"
            else:
                time['warningID'] = "decline deal"

            time['warnTime'] = time['warnTime'].strftime("%m/%d/%Y, %H:%M:%S")
        # self.ids['complaint'].data = ou.getComplaints()
        self.ids['warning'].data = warningTimes

        complaintTimes = ou.getComplaints()
        # for warningtype in complaintTimes:
        #     warningtype['warningID']
        for times in complaintTimes:
            times['compliantTime'] = times['compliantTime'].strftime("%m/%d/%Y, %H:%M:%S")
        self.ids['complaint'].data = complaintTimes
        print("Refresh")

##################################################### SU Pages #################################################
class suItemPost(Screen):
    def declineItem(self):
        print("Decline: %d" % self.itemID)
        su.manageItem(self.itemID, False,self.ids['justification'].text)
        root.getSUitem()
    def approveItem(self):
        print("Approve: %d" %self.itemID)
        su.manageItem(self.itemID, True)
        root.getSUitem()

class suItemSale(Screen):
    def removeItem(self):
        print("Remove: %d" % self.itemID)
        su.removeItem(self.itemID)
        root.getSUitem()

########################################### Blacklist and Taboo Pages ################################################
class blackTaboo(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"

    def addTabooWord(self):
        # check input is not empty
        if guest.checkInput(self.ids['tabooWord'].text):
            self.warnShow = True
        else:
            su.addTaboo(self.ids['tabooWord'].text)
            self.ids['tabooWord'].text = ""
            self.warnShow = False
            root.ids['blackTaboo'].blackListData()

    def blackListData(self):
        self.ids['tabooList'].data = su.getTabooList()
        self.ids['userBlackList'].data = su.getUserBlackList()
        self.ids['itemBlackList'].data = su.getItemBlackList()


class suTransaction(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"
    def Transactions(self):
        self.ids['transactions'].data = su.getTransaction() #data selection to be fixed
                                                            #connections done

################################### Others ################################

class itemManage(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"

class itemFixed(Screen):
    status = BooleanProperty()

class processCompliant(Screen):
    def tohome(self):
        root.ids['screenmanager'].current = "suHomepage"

    def displayComplain(self):
        complains = [{'userID': 'userID1', 'itemID': 'itemID1', 'complain': 'shipping too slow', 'time': '3:00'},
                     {'userID': 'userID2', 'itemID': 'itemID2', 'complain': 'too expensive', 'time': '3:00'}]

        self.ids['complains'].data = complains


    def approveComplain(self):
        print("Approve")
        pass

    def rejectComplain(self):
        print("Reject")
        pass





        
####################### TO BE FILLED #################
class editPassword(FloatLayout):
    back = ObjectProperty(None)
    submit = ObjectProperty(None)


class transactionHistory(Screen):

    # data1 = { 'cancel': True}
    # data2 = { 'accept': True}
    def backProfile(self):
        root.toProfile()
    def OTransactions(self,id):
        data1 = [{'title': str(1), 'price': '1000', 'date': '2019',
        'seller': str(1), 'cancel': True}]
        data2 = [{'title': str(1), 'price': '1000', 'date': '2019',
        'seller': str(1), 'cancel': True}]
        # self.ids['bought'].data = su.viewTransactionHistory1(self,id) #data selection to be fixed
        # self.ids['sold'].data = su.viewTransactionHistory2(self,id) #data selection to be fixed
        self.ids['bought'].data = data1
        self.ids['bought'].data = data2
class fixedItem(Screen):
    itemIndex = NumericProperty()
    user = BooleanProperty()

    def tohome(self):
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].clear()
        self.ids["purchase"].ids["purchaseManager"].current = "empty"
        root.tohome()

    def dislikeItem(self,name):
        root.dislikeItem(name,self.itemIndex)

    def likeItem(self,name):
        root.likeItem(name,self.itemIndex)

    def purchasing(self):
        # purchase Item
        self.ids["purchase"].ids["purchaseManager"].current = "empty"

    def cancelPurchase(self):
        self.purchased = False
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].ids["purchaseManager"].current = "cancel"

    def toPurchase(self):
        item = items[self.itemIndex]
        numWant = int(self.ids["purchaseInfo"].text)
        purchaseInfo = [item.price,numWant ]
        purchaseInfo.extend(ou.calculatePurchase(item.itemID,item.price,numWant))

        self.purchased = True
        self.ids["purchase"].infoLoad(purchaseInfo)
        self.ids["purchase"].ids["purchaseManager"].current = "Purchase"



class biddingItem(Screen):
    itemIndex = NumericProperty()
    user = BooleanProperty()
    def tohome(self):
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].clear()
        self.ids["purchase"].ids["purchaseManager"].current = "empty"
        root.tohome()

    def dislikeItem(self,name):
        root.dislikeItem(name,self.itemIndex)
    def likeItem(self,name):
        root.likeItem(name,self.itemIndex)

    def bidding(self):
        # purchase Item
        self.ids["purchase"].ids["purchaseManager"].current = "empty"

    def cancelbid(self):
        self.bid = False
        self.ids["purchaseInfo"].text = ""
        self.ids["purchase"].ids["purchaseManager"].current = "cancel"

    def toPurchase(self):
        item = items[self.itemIndex]
        # numWant = 1
        bidprice = float(self.ids["purchaseInfo"].text)
        purchaseInfo = [bidprice, 1]
        purchaseInfo.extend(ou.calculatePurchase(item.itemID,bidprice,1))

        self.bid = True
        self.ids["purchase"].infoLoad(purchaseInfo)
        self.ids["purchase"].ids["purchaseManager"].current = "Purchase"

####################### Main Class #############################

class Manager(Screen):
    login = BooleanProperty()
    ouID = ObjectProperty()
    sort = 1
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.displayItem()          # Display Item


    ####################### Display Homepage Item #############################

    def displayItem(self):
        global items
        items = general.popularItem()
        self.sortItem(self.sort)              # Sort by popular Item

    ####################### Search Homepage Item #############################
    def searchKeyword(self, word):
        if word == "":
            self.displayItem()
        else:
            global items
            items = general.searchItem(word)

            if ou is not None:
                print("Not None")
                ou.searchAdd(word)

            if items:
                self.sortItem(self.sort)
            else:
                self.ids['homeItem'].data = []
                print("No result for %s" % word)

    ####################### Sort Homepage Item #############################
    def sortItem(self, sortType):
        global items
        self.sort = sortType
        if sortType == 1:       # By popular views
            items = general.sortItem(items, 'views',decs=True)
        elif sortType == 2:     # By Rating
            items = general.sortItem(items, 'rating',decs=True)
        elif sortType == 3:     # By low to high price
            items = general.sortItem(items, 'price',decs=False)
        elif sortType == 4:     # By high to low price
            items = general.sortItem(items, 'price', decs=True)
        self.itemShow()

    def itemShow(self):
        global items
        returndict = []
        i = 0
        if items:
            for item in items:
                typeStr = "Bidding" if item.priceType else "Fixed Price"
                returndict.append(
                    {"itemIndex": i, "image": item.image, "title": item.title, "priceType": item.priceType,
                     "price": str(item.price), "reviews": str(item.views), "likes": str(item.likeness),
                     "typeStr": typeStr, "rating": str(item.rating)})
                i += 1
            self.ids['homeItem'].data = returndict
    ####################### Homepage Two Button #############################

    def tologin(self):
        if self.login:
            self.login = False
            global ou
            ou = None
        else:
            self.ids['screenmanager'].current = "loginpage"
    def signProfile(self):
        if self.login:
            self.toProfile()
        else:
            self.signup()


    ####################### Login Page Function #############################

    def clearLogin(self):
        self.ids['loginUsername'].text = ""
        self.ids['loginPassword'].text = ""

    def cancelLogin(self):
        self.clearLogin()
        self.ids['screenmanager'].current = "homepage"
    def suLogout(self):
        self.login = False
        global su
        su = None
        self.tohome()

    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        userInfo = general.login_check(username,password)

        if isinstance(userInfo, dict): # Success Login
            self.login = True
            self.ids['loginCheck'].text = ""
            if userInfo['userType']:   # Create SU
                global su
                su = SU(cnx=cnx, cursor=cursor,suID=userInfo['ID'])
                self.ids['screenmanager'].current = "suHomepage"
                self.clearLogin()  # clear login info for potential next user
            else:
                self.ouID = userInfo['ID']
                if userInfo['status'] >= 2: # suspend or in blacklist
                    self.login = False
                    appeal = appealPop()
                    if userInfo['status'] == 3: # in blacklist
                        appeal.ids["appealManager"].current = 'removed'
                    appeal.open()
                else:                   # Create OU
                    global ou
                    ou = OU(cnx=cnx, cursor=cursor,ouID = self.ouID)
                    self.ids['screenmanager'].current = "homepage"
                    self.clearLogin()  # clear login info for potential next user

        else:   # Problem With Login
            self.login = False
            if userInfo == 1:
                self.ids['loginCheck'].text = "Your password is incorrect!!!"
            elif userInfo == 2:
                self.ids['loginCheck'].text = "Your application is still pending."
            elif userInfo == 3:
                self.ids['loginCheck'].text = "You are in the Blacklist!!!"
            else:
                self.ids['loginCheck'].text ="No User Found"


    ####################### Goto OU Profile #############################

    def toProfile(self):
        status = "VIP" if ou.status else "Ordinary User"
        self.ids['ouName'].text = "Name: %s" % ou.name
        self.ids['ouPhone'].text = "Phone: %s" % ou.phone
        self.ids['ouEmail'].text = "Email: %s"% ou.email
        self.ids['ouCard'].text = "Card Number: %s"% ou.card
        self.ids['ouAddress'].text = "Address: %s"% ou.address
        self.ids['ouState'].text = "State: %s"% ou.state
        self.ids['ouRate'].text = "Current Rating: %s"% ou.avgRate
        self.ids['ouMoney'].text = "Current Money Spend: %s"% ou.moneySpend
        self.ids['ouStatus'].text = "Current Status: %s"% status
        self.ids['ouStatusTime'].text = "Status Start Time: {:%b %d, %Y}".format(ou.statusTime)
        self.ids['screenmanager'].current = "profilePage"

    def editInfo(self):
        self.ids['editName'].text =  ou.name
        self.ids['editPhone'].text = ou.phone
        self.ids['editEmail'].text = ou.email
        self.ids['editCard'].text = ou.card
        self.ids['editAddress'].text = ou.address
        self.ids['editState'].text = ou.state
        self.ids['screenmanager'].current = "editPage"

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
        ou.changePassword(newpassword)
        self.dismiss_popup()

    def changeInfo(self,name, card, email, phone, address, state):
        # Need Check....... inputs, add warning label
        ou.updateOUInfo(name, card, email, phone, address, state)
        self.toProfile()


    ###################### To Item Page from homepage ###################
    def checkDisable(self, itemID):
        if ou is not None:
            if general.checkOwner(ou.ID,itemID):
                return False
        return True

    def tofixedItem(self,itemIndex):
        item = items[itemIndex]
        item.addView()
        self.ids['fixedItem'].itemIndex = itemIndex
        self.ids['fixedItem'].user = not self.login
        self.ids['fixedItem'].ids['itemImage'].texture = item.image
        self.ids['fixedItem'].ids['itemTitle'].text = item.title
        self.ids['fixedItem'].ids['itemDescription'].text=item.descrpition
        self.ids['fixedItem'].ids['itemPrice'].text="$"+str(item.price)
        self.ids['fixedItem'].ids['itemAvailable'].text = str(item.available)
        self.ids['fixedItem'].ids['itemLike'].text = str(item.likeness)
        self.ids['fixedItem'].ids['itemDislike'].text = str(item.dislike)
        self.ids['fixedItem'].disableAction = self.checkDisable(item.itemID)

        self.ids['screenmanager'].current = "fixedItem"

    def tobidItem(self,itemIndex):
        item = items[itemIndex]
        item.addView()
        self.ids['biddingItem'].user = not self.login
        self.ids['biddingItem'].itemIndex = itemIndex
        self.ids['biddingItem'].ids['itemImage'].texture = item.image
        self.ids['biddingItem'].ids['itemTitle'].text = item.title
        self.ids['biddingItem'].ids['itemDescription'].text=item.descrpition
        self.ids['biddingItem'].ids['itemPrice'].text="$"+str(item.price)
        self.ids['biddingItem'].ids['itemLike'].text = str(item.likeness)
        self.ids['biddingItem'].ids['itemDislike'].text = str(item.dislike)
        self.ids['biddingItem'].ids['itemUsed'].text = str(item.usedStatus)
        self.ids['biddingItem'].disableAction = self.checkDisable(item.itemID)
        try:
            self.ids['biddingItem'].ids['itemBid'].text = "$" + str(item.highestPrice)
        except AttributeError:
            self.ids['biddingItem'].ids['itemBid'].text = "None"
        self.ids['screenmanager'].current = "biddingItem"

    ############################# Like/Dislike Item ################################
    def likeItem(self,pagename,itemIndex):
        items[itemIndex].likeItem(ou.ID)
        self.ids[pagename].ids['itemLike'].text = str(items[itemIndex].likeness)

    def dislikeItem(self,pagename,itemIndex):
        items[itemIndex].dislikeItem(ou.ID)
        self.ids[pagename].ids['itemDislike'].text = str(items[itemIndex].dislike)

    ################################### OU Item Page ################################
    def getOUitem(self):
        ouItems = ou.getItem()
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

        self.ids["ouItem"].ids["waitItem"].data = waitI
        self.ids["ouItem"].ids["itemFixed"].data = fixedI
        self.ids["ouItem"].ids["itemBid"].data = bidI

    ################################### Friend Page ################################
    def friendList(self):
        print('friendlist')
        root.ids["friendPage"].selectedFriend = " Unselected "
        self.ids["friendPage"].ids['warn'].text = ""
        self.ids["friendPage"].ids['friends'].data = ou.getFriend()
        self.ids["friendPage"].ids['messages'].data = []


        self.ids['screenmanager'].current = "friendPage"

    def getMessage(self,friendID):
        messages = ou.getFriendMessage(friendID)
        self.friendID = friendID
        for mess in messages:
            mess['sendTime'] = mess['sendTime'].strftime("%H:%M:%S")
        root.ids["friendPage"].ids['messages'].data = messages



    ################################### SU Item Page ################################
    def getSUitem(self):
        suItems = su.getAllItem()
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


    def tohome(self):
        self.displayItem()
        self.ids['screenmanager'].current = "homepage"


    def signup(self):
        self.ids['screenmanager'].current = "signupPage"
    def history(self):
        print('history')
        # self.ids['history'].OTransactions(root.ouID)
        self.ids['screenmanager'].current = "historyPage"



    def toguApply(self):
        self.ids['guApply'].getApplications()
        self.ids['screenmanager'].current = "GUapplication"


    def toouInfo(self):
        self.ids['ouInfo'].getOUInformation()
        self.ids['screenmanager'].current = "ouInfo"
    def toitemManage(self):
        self.getSUitem()
        self.ids['screenmanager'].current = "itemManage"

    def toOuItem(self):
        self.getOUitem()
        self.ids['screenmanager'].current = "ouItem"
    def toWarning(self):
        self.ids['ouWarning'].warningData()
        self.ids['screenmanager'].current = "ouWarning"

    def toCompliant(self):
        self.ids['screenmanager'].current ="processCompliant"

    def toBlacklist(self):
        self.ids['blackTaboo'].blackListData()
        self.ids['screenmanager'].current = "blackTaboo"
    def toSUtransaction(self):
        self.ids['screenmanager'].current = "suTransaction"
        self.ids['suTransaction'].Transactions()

class eByMazonApp(App):

    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Builder.load_file("manage.kv")
        global root
        root = Manager()
        return root

if __name__ == "__main__":
    config = {
        "user": 'eby',                 # Enter your own username
        "password": 'ebypw',             # Enter your own password
        "host": '127.0.0.1',
        "database": 'eByMazon'
    }

    try:
        cnx = mysql.connector.connect(**config)
        cnx.set_unicode(value=True)
        cursor = cnx.cursor(buffered=True)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        raise err

    general = General(cnx=cnx,cursor=cursor)
    guest = GU(cnx=cnx,cursor=cursor)
    ou,su,items = None,None,None
    eByMazonApp().run()