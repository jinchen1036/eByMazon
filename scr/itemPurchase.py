from kivy.uix.screenmanager import Screen
# self define classes

class FixedPurchase(Screen):
    def clear(self):
        self.singlePrice = 0
        self.numberBuy = 0
        self.tax = 0
        self.vip = 0
        self.friend = 0
        self.finalPrice =0
        self.purchased = False

    def infoLoad(self, priceInfo):
        self.singlePrice = priceInfo[0]
        self.numberBuy = priceInfo[1]
        self.tax = round(priceInfo[3],3)
        self.friend = round(priceInfo[4],3)
        self.vip = round(priceInfo[5],3)
        self.finalPrice = round(priceInfo[6],3)
        self.purchased = True

class BidPurchase(Screen):
    def clear(self):
        self.bidPrice = 0
        self.tax = 0
        self.vip = 0
        self.friend = 0
        self.finalPrice =0
        self.purchased = False

    def infoLoad(self, priceInfo):
        self.bidPrice = round(priceInfo[0],3)
        self.tax = round(priceInfo[3],3)
        self.friend = round(priceInfo[4],3)
        self.vip = round(priceInfo[5],3)
        self.finalPrice = round(priceInfo[6],3)
        self.purchased = True