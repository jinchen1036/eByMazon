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
        globalV.root.ids["friendPage"].initInfo()
        globalV.root.ids["friendPage"].selectedFriend = self.username
        globalV.root.ids["friendPage"].displayMessage(self.friendID)
        # print(self.friendID)

class friendRequest(GridLayout):
    def getFriendMessage(self):
        globalV.root.ids["friendPage"].initInfo()
        globalV.root.ids["friendPage"].selectedFriend = self.username
        globalV.root.ids["friendPage"].displayMessage(self.friendID)

    def addFriend(self):
        discount = self.ids['discount'].text
        discount = 5 if discount =='' else discount
        globalV.root.ids["friendPage"].addFriend(self.username,discount)
        globalV.root.ids["friendPage"].ids['friendReq'].data = globalV.ou.getFriendRequest()
        print("Add")

class friendList(Screen):
    def initInfo(self):
        self.selectedFriend = " Unselected "
        self.ids['chat'].text = ""
        self.ids['friends'].data = globalV.ou.getFriend()
        self.ids['friendReq'].data = globalV.ou.getFriendRequest()#[{'friendID':1,'username':'xxx'}]
        self.ids['messages'].data = []
        self.clearMsg()

    def backProfile(self):
        self.initInfo()
        globalV.root.toProfile()

    def displayFriend(self):
        self.ids['friends'].data = globalV.ou.getFriend()
        self.ids['friendReq'].data = globalV.ou.getFriendRequest()


    def clearMsg(self):
        self.ids['warning'].text = ''
        self.ids['friendName'].text = ''
        self.ids['discount'].text = ''
        self.ids['warn'].text=''

    def addFriend(self, username, discount):
        if not globalV.general.checkFloat(discount):
            self.ids['warning'].text = 'Please enter valid input for discount'
        elif globalV.guest.checkUsername(username) != 1 or not globalV.guest.checkUsername(username):
            self.ids['warning'].text = 'Please enter valid username'
        else:
            if float(discount) < 100:
                self.clearMsg()
                friendID = globalV.general.getID(username)
                globalV.ou.addFriend(friendID, round(float(discount)/100,2))
                print("Add Friend, Discount: ", float(discount)/100)
                self.displayFriend()
            else:
                self.ids['warning'].text = 'Discount must below 100%'


    def displayMessage(self,friendID):
        self.clearMsg()
        messages = globalV.ou.getFriendMessage(friendID)
        self.friendID = friendID
        for mess in messages:
            mess['sendTime'] = mess['sendTime'].strftime("%m/%d %H:%M")
        self.ids['messages'].data = messages


    def sentMessage(self,message):
        if self.selectedFriend == " Unselected ":
            self.ids['send'].disable = True
            self.ids['warn'].text = "Please Select a Friend"
        elif self.ids['chat'].text =="":
            self.ids['send'].disable = True
            self.ids['warn'].text = "Can't send empty message"
        elif self.friendID not in globalV.ou.friendIDs:
            self.ids['send'].disable = True
            self.ids['warn'].text = "Can't send message without add friend."
        else:
            self.ids['chat'].text = ""
            self.ids['warn'].text = ""
            self.ids['send'].disable = False
            globalV.ou.sendFriendMessage(self.friendID,message)

            self.displayMessage(self.friendID)
