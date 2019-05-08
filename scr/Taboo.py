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

    def changeLabel(self,label):
        self.ids['taboo'].text = label

    # def change_to_star(self,input):
    #
    #     ''' pre-condition: if input contains taboo
    #         params: userInput and taboo contained
    #         return: string with taboo replaced
    #     '''
    #
    #     taboos = globalV.general.findtaboo(input)
    #     if not taboos:
    #         return False
    #
    #     for taboo in taboos:
    #         taboo = taboo.lower()
    #         input = input.lower()
    #         input.replace('taboo', '*'*len(taboo))
    #
    #     return input

    # def get_taboo(self, input):
    #     qry = ( "SELECT word FROM Taboo ON %s LIKE CONCAT('%', word ,'%') ;") % input


    #     qry = ('SELECT * FROM Taboo')
    #     self.cursor.execute(qry)

    #     pass

    # def switchScreen(self, screenName):
    #     self.ids['appealManager'].current = screenName


