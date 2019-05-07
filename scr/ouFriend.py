from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV


################################################## Friend Page ###############################################

class friendInfo(GridLayout):
    def deleteFriend(self):
        # print(self.friendID)

        test = globalV.ou.deleteFriend(self.friendID)
        globalV.root.ids["friendPage"].displayFriend()

    def getFriendMessage(self):
        globalV.root.ids["friendPage"].selectedFriend = self.username
        globalV.root.ids["friendPage"].displayMessage(self.friendID)
        # print(self.friendID)

class friendList(Screen):
    def initInfo(self):
        self.selectedFriend = " Unselected "
        self.ids['chat'].text = ""
        self.ids['friends'].data = globalV.ou.getFriend()
        self.ids['messages'].data = []
        self.clearMsg()

    def backProfile(self):
        self.initInfo()
        globalV.root.toProfile()

    def displayFriend(self):
        friends = globalV.ou.getFriend()
        self.ids['friends'].data = friends


    def clearMsg(self):
        self.ids['warning'].text = ''
        self.ids['friendName'].text = ''
        self.ids['discount'].text = ''

    def addFriend(self, username, discount):
        if not globalV.guest.checkUsername(username) or not globalV.general.checkFloat(discount):
            print(globalV.guest.checkUsername(username))
            print(globalV.general.checkFloat(discount))
            self.ids['warning'].text = 'Please enter valid input'
        else:
            if float(discount) < 100:
                self.clearMsg()
                friendID = globalV.general.getID(username)
                globalV.ou.addFriend(friendID, float(discount)/100)
                print("Add Friend, Discount: ", float(discount)/100)
                self.displayFriend()
            else:
                self.ids['warning'].text = 'Discount must below 100%'


    def displayMessage(self,friendID):
        messages = globalV.ou.getFriendMessage(friendID)
        self.friendID = friendID
        for mess in messages:
            mess['sendTime'] = mess['sendTime'].strftime("%H:%M:%S")
        self.ids['messages'].data = messages


    def sentMessage(self,message):
        if self.selectedFriend == " Unselected ":
            self.ids['send'].disable = True
            self.ids['warn'].text = "Please Select a Friend"
        elif self.ids['chat'].text =="":
            self.ids['send'].disable = True
            self.ids['warn'].text = "Can't send empty message"
        else:
            self.ids['chat'].text = ""
            self.ids['warn'].text = ""
            self.ids['send'].disable = False
            globalV.ou.sendFriendMessage(self.friendID,message)

            self.displayMessage(self.friendID)
