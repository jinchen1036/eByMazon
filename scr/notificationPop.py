from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV


class notificationPop(Popup):
    def dismissPop(self):
        self.ids['messageShow'].text =""
        notificationPop.dismiss(self)

    def checkNotificationitem(self):
        noti = globalV.general.checkNotification()
        if noti != "":
            self.ids['messageShow'].text += "\nKeywords search by other users: \n      "+noti

    def checkVIPchange(self):
        if globalV.ou.promote:
            self.ids['messageShow'].text += "\n\nCongratulation, You have be promote to VIP!!!\n\n"
        elif globalV.ou.depromote:
            self.ids['messageShow'].text += "\n\nYou have be depromote to ordinary user!!!\n\n"


