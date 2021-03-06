from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty,NumericProperty,ObjectProperty

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV
################################################## Sign Up Page ###############################################
class Signup(Screen):
    # sign up page implement in signup.kv
    stateV,cardV,nameV,phoneV = BooleanProperty(),BooleanProperty(),BooleanProperty(),BooleanProperty()

    def tohome(self):
        globalV.root.tohome()

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
        self.stateV, self.cardV, self.nameV,self.phoneV = True, True,True,True

    def checkUsername(self,username):
        nameCheck = globalV.guest.checkUsername(username)
        if not nameCheck:
            self.ids['warnUsername'].text = "Username can be used"
        elif nameCheck == 1:
            self.ids['warnUsername'].text = "Username already existed in system"
        elif nameCheck == 2:
            self.ids['warnUsername'].text = "Username already existed in system"
        elif nameCheck == 3:
            self.ids['warnUsername'].text = "Username are in system blacklist!"

    def checkName(self,name):
        self.nameV = globalV.general.checkEmpty(name)

    def checkState(self,state):
        self.stateV = globalV.guest.checkState(state.upper())

    def checkCard(self,card):
        self.cardV = globalV.general.checkInt(card)
        if self.cardV:
            self.cardV = (len(card) == 16)
    def checkPhone(self,phone):
        self.phoneV = globalV.general.checkInt(phone)
        if self.phoneV:
            self.phoneV = (len(phone) == 10)

    def signUp(self,username, name, phone, email,address,state,card):
        found1 = globalV.root.replaceTaboo(username)
        found2 = globalV.root.replaceTaboo(name)
        found3 = globalV.root.replaceTaboo(address)

        tabooFound = found1 or found2 or found3
        if tabooFound:
            replaceWord = ''
            if found1:
                self.ids['GUusername'].text = ""
                replaceWord += "Taboo in username: %s \n" %found1
            if found2:
                self.ids['GUname'].text = ""
                replaceWord += "Taboo in name: %s \n" % found2
            if found3:
                self.ids['GUaddress'].text = ""
                replaceWord += "Taboo in address: %s \n" % found3

            globalV.root.toTaboo(replaceWord)

        self.checkName(name)
        self.checkState(state)
        self.checkCard(card)
        self.checkUsername(username)
        self.checkPhone(phone)



        if globalV.guest.checkUsername(username) or not self.stateV or not self.cardV or not self.nameV or not self.phoneV or tabooFound:
            self.ids['warnApplication'].text = "Fail to Apply!!!"
        else:
            applied = globalV.guest.apply(username, name, email,card,address,state.upper(),phone)
            self.ids['warnApplication'].text = "Fail to Apply!!!" # for not approve application
            if applied:                                      # save on DB
                self.ids['warnApplication'].text = ""
                self.clearSignup()
                globalV.root.tohome()

class editProfile(Screen):
    def toProfile(self):
        globalV.root.toProfile()
    def editInfo(self):
        self.ids['editName'].text =  globalV.ou.name
        self.ids['editPhone'].text = globalV.ou.phone
        self.ids['editEmail'].text = globalV.ou.email
        self.ids['editCard'].text = globalV.ou.card
        self.ids['editAddress'].text = globalV.ou.address
        self.ids['editState'].text = globalV.ou.state
        self.valid = False

    def checkName(self,name):
        self.nameV = globalV.general.checkEmpty(name)

    def checkState(self,state):
        self.stateV = globalV.guest.checkState(state.upper())

    def checkCard(self,card):
        self.cardV = globalV.general.checkInt(card)
        if self.cardV:
            self.cardV = (len(card) == 16)
    def checkPhone(self,phone):
        self.phoneV = globalV.general.checkInt(phone)
        if self.phoneV:
            self.phoneV = (len(phone) == 10)

    def changeInfo(self,name, card, email, phone, address, state):
        # Need Check....... inputs, add warning label

        if not (globalV.general.checkEmpty(name) or globalV.guest.checkState(state.upper())):
            self.valid = True
        elif not globalV.guest.checkState(state)  or len(card) != 16 or len(phone) != 10:
            self.valid = True
        elif not(globalV.general.checkInt(card) or globalV.general.checkInt(phone)):
            self.valid = True
        else:
            found1 = globalV.root.replaceTaboo(name)
            found2 = globalV.root.replaceTaboo(address)

            tabooFound = found1 or found2
            if tabooFound:
                replaceWord = ''
                if found1:
                    self.ids['editName'].text = ""
                    replaceWord += "Taboo in name: %s \n" % found1
                if found2:
                    self.ids['editAddress'].text = ""
                    replaceWord += "Taboo in address: %s \n" % found2

                globalV.root.toTaboo(replaceWord)
                globalV.ou.addWarning(warningID=4, description='Taboo word in edit profile info')
            else:
                globalV.ou.updateOUInfo(name, card, email, phone, address, state)
                self.toProfile()