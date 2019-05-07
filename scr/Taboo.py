from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV


class tabooPop(Popup):
    def dismissPop(self):
        tabooPop.dismiss(self)
        # globalV.root.ids['login'].clearLogin()
        # globalV.root.tohome()

    # def switchScreen(self, screenName):
    #     self.ids['appealManager'].current = screenName


