from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

try:
    from scr.GlobalVariable import globalV
    from scr.OU import OU
    from scr.SU import SU
    from scr.notificationPop import notificationPop
except ModuleNotFoundError:
    from GlobalVariable import globalV
    from OU import OU
    from SU import SU
    from notificationPop import notificationPop

class appealPop(Popup):
    def homepage(self):
        appealPop.dismiss(self)
        globalV.root.ids['login'].clearLogin()
        globalV.root.tohome()

    def switchScreen(self, screenName):
        self.ids['appealManager'].current = screenName

    def removeOU(self):
        globalV.general.removeOU(username=globalV.root.ids['login'].ids['loginUsername'].text)
        self.homepage()

    def appeal(self,message):
        globalV.general.appeal(ouID=globalV.root.ouID,message=message)
        self.homepage()

class Login(Screen):
    def clearLogin(self):
        self.ids['loginUsername'].text = ""
        self.ids['loginPassword'].text = ""
        self.newUser = False

    def cancelLogin(self):
        self.clearLogin()
        globalV.ou = None
        globalV.root.tohome()

    def checkLogin(self,username,password):
        print("Username: %s \nPassword: %s" % (username,password))

        if self.newUser:
            if globalV.general.checkEmpty(password):
                globalV.ou.changePassword(password)
                self.initOU()
                print("update password")
            else:
                self.ids['loginCheck'].text ="Cannot have empty password, please re-enter!!!"

        else:
            userInfo = globalV.general.login_check(username,password)

            if isinstance(userInfo, dict): # Success Login
                globalV.root.login = True
                self.ids['loginCheck'].text = ""
                if userInfo['userType']:   # Create SU
                    globalV.su = SU(cnx=globalV.cnx, cursor=globalV.cursor,suID=userInfo['ID'])
                    globalV.root.ids['screenmanager'].current = "suHomepage"
                    self.clearLogin()  # clear login info for potential next user
                else:
                    globalV.root.ouID = userInfo['ID']
                    if userInfo['status'] >= 2: # suspend or in blacklist
                        globalV.root.login = False
                        appeal = appealPop()
                        if userInfo['status'] == 3: # in blacklist
                            appeal.ids["appealManager"].current = 'removed'
                        appeal.open()
                    else:                   # Create OU
                        # global ou
                        globalV.ou = OU(cnx=globalV.cnx, cursor=globalV.cursor, ouID=globalV.root.ouID)

                        if username == password:
                            self.newUser = True
                            self.ids['loginPassword'].text = ""
                            self.ids['loginCheck'].text = "Welcome New User!!! \nPlease enter a new password."
                        else:
                            self.initOU()

            else:   # Problem With Login
                globalV.root.login = False
                if userInfo == 1:
                    self.ids['loginCheck'].text = "Your password is incorrect!!!"
                elif userInfo == 2:
                    self.ids['loginCheck'].text = "Your application is still pending."
                elif userInfo == 3:
                    self.ids['loginCheck'].text = "You are in the Blacklist!!!"
                else:
                    self.ids['loginCheck'].text ="No User Found"

    def initOU(self):
        self.notificationPoo()
        globalV.root.displayOULikeItem()
        globalV.root.ids['screenmanager'].current = "homepage"
        self.clearLogin()  # clear login info for potential next user

    def notificationPoo(self):
        noti = notificationPop()
        noti.checkNotificationitem()
        noti.checkVIPchange()
        if noti.ids['messageShow'].text != "":

            noti.open()