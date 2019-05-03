from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty,NumericProperty,ObjectProperty

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV
################################################## Sign Up Page ###############################################
class Signup(Screen):
    # sign up page implement in signup.kv
    stateV,cardV,nameV = BooleanProperty(),BooleanProperty(),BooleanProperty()

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
        self.stateV, self.cardV, self.nameV = True, True,True

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
        self.nameV = not globalV.guest.checkInput(name)

    def checkState(self,state):
        self.stateV = globalV.guest.checkState(state.upper())

    def checkCard(self,card):
        self.cardV = not globalV.guest.checkInput(card)

    def signUp(self,username, name, phone, email,address,state,card):
        self.checkName(name)
        self.checkState(state)
        self.checkCard(card)
        self.checkUsername(username)
        if globalV.guest.checkUsername(username) or not self.stateV or not self.cardV or not self.nameV:
            self.ids['warnApplication'].text = "Fail to Apply!!!"
        else:
            applied = globalV.guest.apply(username, name, email,card,address,state.upper(),phone)
            self.ids['warnApplication'].text = "Fail to Apply!!!" # for not approve application
            if applied:                                      # save on DB
                self.ids['warnApplication'].text = ""
                self.clearSignup()
                globalV.root.tohome()