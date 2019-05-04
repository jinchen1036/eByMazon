from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV


class rate(FloatLayout):
    submitRate = ObjectProperty(None)
    toHistory = ObjectProperty(None)


class complain(FloatLayout):
    submitComplain = ObjectProperty(None)
    toHistory = ObjectProperty(None)


class bought(GridLayout):
    def dismiss_popup(self):
        self._popup.dismiss()
        globalV.root.ids['history'].getTransaction()

    def complain(self):
        if self.complained:
            self.ids['complain'].current = "text"
        else:
            print('Complain')
            content = complain(toHistory=self.dismiss_popup, submitComplain=self.submitComplain)
            self._popup = Popup(title="Submit Compliant", content=content,
                                size_hint=(0.8, 0.8))
            self._popup.open()

    def rate(self):
        if self.rated:
            self.ids['rating'].current = "text"
        else:
            content = rate(toHistory=self.dismiss_popup, submitRate=self.submitRate)
            self._popup = Popup(title="Submit Rate", content=content,
                                size_hint=(0.8, 0.8))
            self._popup.open()

    def submitComplain(self, description):
        if description != "":
            print(description)
            globalV.ou.submitCompliant(self.itemID,description)
            self.ids['complain'].current = "text"
            self.dismiss_popup()

    def submitRate(self,rating, comment):
        if comment != "":
            globalV.ou.submitRating(self.itemID, rating,comment)
            self.ids['rating'].current = "text"
            self.dismiss_popup()


class sold(GridLayout):
    def acceptPurchase(self):
        print('Accept')
        globalV.ou.acceptSale(self.itemID,self.buyerID,self.price)
        globalV.root.ids['history'].ids['sold'].data = globalV.ou.getSaleHistory()

    def declinePurchase(self):
        print('Decline')
        globalV.ou.declineSale(self.itemID, self.buyerID)
        globalV.root.ids['history'].ids['sold'].data = globalV.ou.getSaleHistory()


class transactionHistory(Screen):
    def backProfile(self):
        print('back')
        globalV.root.toProfile()

    def getTransaction(self):
        self.ids['bought'].data = globalV.ou.getBuyHistory()
        self.ids['sold'].data = globalV.ou.getSaleHistory()
    #---to be filed---#


