from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV



class bought(GridLayout):
    def complain(self):
        print('Complain')
        # self.ids['screenmanager'].current = "rate"
    def rate(self):
        print('Rate')
        # self.ids['screenmanager'].current = "complain"
    pass

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



    def submitComplain(self):
        pass
    def submitRate(self):
        pass