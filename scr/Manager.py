# mysql
import mysql.connector
from mysql.connector import errorcode
# kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen #ScreenManager, FadeTransition
from kivy.properties import BooleanProperty
from kivy.lang import Builder
from kivy.core.window import Window

# self define classes
try:
    from scr.GeneralFunctions import General
    from scr.GU import GU
    from scr.SU import SU
    from scr.OU import OU
    from scr.otherClass import *
except ModuleNotFoundError:
    from GeneralFunctions import General
    from GU import GU
    from SU import SU
    from OU import OU
    from otherClass import *

class item(BoxLayout):
    # the item frame in homepage, implemented in feature.kv
    def getItem(self):
        print(type(self.priceType))

        if self.priceType:
            root.tobidItem(self.itemID, self.title, self.image, self.priceType, self.description)
        else:
            root.tofixedItem(self.itemID,self.title,self.image,self.priceType,self.description)

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
            self.ids['warnUsername'].text = "Username existed in system"
        elif nameCheck == 2:
            self.ids['warnUsername'].text = "Username existed in system"
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

class fixedItem(Screen):
    def tohome(self):
        root.tohome()

class biddingItem(Screen):
    def tohome(self):
        root.tohome()

class Manager(Screen):
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.displayItem()

    # Login Page
    def clearLogin(self):
        self.ids['loginUsername'].text = ""
        self.ids['loginPassword'].text = ""

    def cancelLogin(self):
        self.clearLogin()
        self.ids['screenmanager'].current = "homepage"

    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))
        userInfo = general.login_check(username,password)

        if isinstance(userInfo, dict): # Success Login
            self.login = True
            self.ids['loginCheck'].text = ""
            self.clearLogin()  # clear login info for potential next user

            if userInfo['userType']:   # Create SU
                global su
                su = SU(cursor=cursor,suID=userInfo['ID'])
                self.ids['screenmanager'].current = "suHomepage"
            else:
                if userInfo['status'] == 2:
                    self.login = False
                    print("Suspend OU")
                    self.ids['loginCheck'].text = "You have receive 2 warning!!!\nYou are suspend by our system"
                # need a pop up page for appeal message
                elif userInfo['status'] == 3:
                    self.login = False
                    general.removeOU(ouID=userInfo['ID'],username=username)
                    self.ids['loginCheck'].text = "You have be removed by SU!!!\nYour information is now be delete"
                    print("Remove OU")
                # need to function to delete the OU in DB
                else:                   # Create OU
                    global ou
                    ou = OU(cursor=cursor,ouID = userInfo['ID'])
                    self.ids['screenmanager'].current = "homepage"

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

    # Go to OU Account
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

    def changePassword(self):
        print("Change Password")
    def sortPop(self):
        print("Sort by Popular")
    def sortRating(self):
        print("Sort by Rating")
    def sortPricelh(self):
        print("Sort by price low to high")
    def sortPricehl(self):
        print("Sort by price high to low")

    def displayItem(self):
        self.ids['rv'].data = general.popularItem()


    def tohome(self):
        self.ids['screenmanager'].current = "homepage"
    def tologin(self):
        self.ids['screenmanager'].current = "loginpage"
    def signup(self):
        self.ids['screenmanager'].current = "signupPage"


    def tofixedItem(self,itemID,title,image,priceType,description):
        self.ids['fixedItem'].ids['itemImage'].texture = image
        self.ids['fixedItem'].ids['itemTitle'].text = title
        self.ids['fixedItem'].ids['itemDescription'].text=description
        self.ids['screenmanager'].current = "fixedItem"

    def tobidItem(self,itemID,title,image,priceType,description):
        self.ids['biddingItem'].ids['itemImage'].texture = image
        self.ids['biddingItem'].ids['itemTitle'].text = title
        self.ids['biddingItem'].ids['itemDescription'].text=description
        self.ids['screenmanager'].current = "biddingItem"

    def friendList(self):
        print('friendlist')
        self.ids['screenmanager'].current = "friendPage"
    def history(self):
        print('history')
        self.ids['screenmanager'].current = "historyPage"

    def searchKeyword(self, word):
        self.displayItem()
        print(word)


class eByMazonApp(App):
    # m = Manager()
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        Builder.load_file("manage.kv")
        global root
        root = Manager()
        return root

if __name__ == "__main__":
    config = {
        "user": '',                 # Enter your own username
        "password": '',             # Enter your own password
        "host": '127.0.0.1',
        "database": 'eByMazon'
    }
    try:
        cnx = mysql.connector.connect(**config)
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
    ou = None
    su = None
    eByMazonApp().run()