from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout

try:
    from scr.GlobalVariable import globalV
except ModuleNotFoundError:
    from GlobalVariable import globalV

################################### OU INFO ################################
class ouInformation(BoxLayout):
    def removeOU(self,ouID):
        globalV.su.removeOU(ouID)
        globalV.root.ids['ouInfo'].getOUInformation()

class ouInfo(Screen):
    def tohome(self):
        globalV.root.ids['screenmanager'].current = "suHomepage"

    def getOUInformation(self):
        ous = globalV.su.getOU()
        ouData = []
        for ou in ous:
            remove = True if ou.status == 3 else False
            status = 'Ordinary'
            if ou.status == 1:
                status = 'VIP'
            elif ou.status == 2:
                status = 'Suspend'
            elif ou.status == 3:
                status = 'Removed'

            ouData.append({'ouID': ou.ID, 'ouName': ou.name, 'ouPhone': ou.phone, 'ouEmail': ou.email,
                           'ouCard': ou.card, 'ouAddress': ou.address,'ouState':ou.state,
                           'ouStatus':status, 'ouRate': ou.avgRate, 'ouComplaint': len(ou.compliants),
                           'ouWarning': 0, 'remove': remove})
        self.ids['ouInformation'].data = ouData

############################################## OU Warning Page #################################################
class ouWarning(Screen):
    def tohome(self):
        globalV.root.ids['screenmanager'].current = "profilePage"

    def warningData(self):
        warningTimes = globalV.ou.getWarnings()
        for time in warningTimes:
            if (time['warningID'] == 0):
                time['warningID'] = "reckless graders"
            elif (time['warningID'] == 1):
                time['warningID'] = "complaints"
            elif (time['warningID'] == 2):
                time['warningID'] = "decline deal"
            elif (time['warningID'] == 3):
                time['warningID'] = "item removed by su"
            else:
                time['warningID'] = "use taboo word"

            # time['warnTime'] = time['warnTime'].strftime("%m/%d/%Y, %H:%M:%S")
        # self.ids['complaint'].data = globalV.ou.getComplaints()
        self.ids['warning'].data = warningTimes

        complaintTimes = globalV.ou.getComplaints()
        # for warningtype in complaintTimes:
        #     warningtype['warningID']
        # for times in complaintTimes:
        #     times['compliantTime'] = times['compliantTime'].strftime("%m/%d/%Y, %H:%M:%S")
        self.ids['complaint'].data = complaintTimes
        # print("Refresh")
