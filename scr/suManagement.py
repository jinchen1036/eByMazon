from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV


################################### GU Application ################################
class GUapplication(Screen):
    def tohome(self):
        globalV.root.ids['screenmanager'].current = "suHomepage"

    def getApplications(self):
        self.ids['application'].data = globalV.su.getGU()
        # print("Refresh")

class guApplications(BoxLayout):
    def manageApplication(self,guUsername, action):
        globalV.su.manageApplication(guUsername, action)

##################################################### SU Pages #################################################
class suItemPost(Screen):
    def declineItem(self):
        print("Decline: %d" % self.itemID)
        globalV.su.manageItem(self.itemID, False,self.ids['justification'].text)
        globalV.root.getSUitem()
    def approveItem(self):
        print("Approve: %d" %self.itemID)
        globalV.su.manageItem(self.itemID, True)
        globalV.root.getSUitem()

class suItemSale(Screen):
    def removeItem(self):
        print("Remove: %d" % self.itemID)
        globalV.su.removeItem(self.itemID)
        globalV.root.getSUitem()

########################################### Blacklist and Taboo Pages ################################################
class blackTaboo(Screen):
    def tohome(self):
        globalV.root.ids['screenmanager'].current = "suHomepage"

    def addTabooWord(self):
        # check input is not empty
        if globalV.guest.checkInput(self.ids['tabooWord'].text):
            self.warnShow = True
        else:
            globalV.su.addTaboo(self.ids['tabooWord'].text)
            self.ids['tabooWord'].text = ""
            self.warnShow = False
            globalV.root.ids['blackTaboo'].blackListData()

    def blackListData(self):
        self.ids['tabooList'].data = globalV.su.getTabooList()
        self.ids['userBlackList'].data = globalV.su.getUserBlackList()
        self.ids['itemBlackList'].data = globalV.su.getItemBlackList()



class itemManage(Screen):
    def tohome(self):
        globalV.root.ids['screenmanager'].current = "suHomepage"