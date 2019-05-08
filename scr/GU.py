# Functions in this GU Class
# - checkUsername(self,username)
# - checkState(self,state)
# - checkInput(self,input)
# - apply(self, username, name, email, card, address, state, phone)


import mysql.connector
class GU():
    def __init__(self,cnx,cursor):
        self.cnx = cnx
        self.cursor = cursor

    def checkUsername(self,username):
        '''
        :param username: username for check if exist in account DB, application DB, blacklist
        :return:
            -   1                               found in accountDB
            -   2                               found in GU application
            -   3                               found in blacklist
            -   False                           nothing found
        '''
        # check for not match password
        qry = "SELECT EXISTS(SELECT * from User WHERE username='%s');" % username
        self.cursor.execute(qry)
        if self.cursor.fetchone()[0]:
            return 1    # found in accountDB

        # check for application waiting
        qry = "SELECT EXISTS(SELECT * from GUapplications WHERE username='%s');" % username
        self.cursor.execute(qry)
        if self.cursor.fetchone()[0]:
            return 2    # found in GU application

        # check if in blacklist
        qry = "SELECT EXISTS(SELECT * from ouBlacklist WHERE ouName='%s');" % username
        self.cursor.execute(qry)
        if self.cursor.fetchone()[0]:
            return 3    # found in blacklist

        return False        # nothing found

    def checkState(self,state):
        '''
        :param state:
        :return: bool
            -   True               Found in Tax DB
            -   False              Not Found in Tax DB
        '''
        qry = "SELECT EXISTS(SELECT * from Tax WHERE state='%s');" % state
        self.cursor.execute(qry)
        if self.cursor.fetchone()[0]:
            return True    # found in state tax
        return False

    def checkInput(self,input):
        """
        :param card:
        :return:
            - True                  input is empty string
            - False                 input is not empty string
        """
        if input is None or input == "":
            return True
        return False

    def apply(self, username, name, email, card, address, state, phone):
        '''
        :param username:
        :param name:
        :param email:
        :param card:
        :param address:
        :param state:
        :param phone:
        :return:
            -   True               Success apply
            -   False              Fail to apply
        '''
        try:
            qry = ("INSERT INTO GUapplications( username, email, name, cardNumber, address, state, phone) "
                   "VALUE (%s,%s,%s,%s,%s,%s,%s);")
            self.cursor.execute(qry,(username, email, name, card, address, state, phone))
            self.cnx.commit()
            return True
        except mysql.connector.Error as ERR:
            print("Error in Applying OU Account: %s" % ERR)
            return False

