import json
from utils import write_json_file, open_json_file
import sys

class Commission:
    def __init__(self, filepath : str):
        self.writeFile = filepath
        self.data = {}

    def getData(self, filepath : str):
        '''
        Open json file and set class variable with the content.

        :param self: class member functions and variables.
        :param filepath: name and path of the file.
        :return: nothing.
        '''

        self.data = open_json_file(filepath)

    def getDealsFromId(self, userId : int) -> dict:
        '''
        Get all deals for one user.

        :param self: class member functions and variables.
        :param userId: id of the user.
        :return: dict with the user and all deals that he closed.
        '''
        userDeals = []
        for deal in self.data['deals']:
            if deal['user'] == userId:
                userDeals.append(deal)
        return {"userId" : userId, "deals": userDeals}

    def getAllDeals(self) -> list[dict]:
        '''
        Get all deals for one user.

        :param self: class member functions and variables.
        :param: none.
        :return: list of dict with users and deals.
        '''
        deals = []

        for user in self.data['users']:
            deals.append(self.getDealsFromId(user['id']))
        return deals

    def getPaymentMonths(self, userDeals : dict) -> list[str]:
        '''
        Get all payment months for list of deals.

        :param self: class member functions and variables.
        :param userDeals: list of deals of one user.
        :return: list with all the payment months.
        '''

        months = []
        for deal in userDeals:
            months.append(deal['payment_date'][0:-3])
        return list(dict.fromkeys(months))

    def getDealFromMonths(self) -> list[dict]:
        '''
        Get all payment months for list of deals.

        :param self: class member functions and variables.
        :param userDeals: list of deals of one user.
        :return: list with all the payment months.
        '''
        UsersDeals = self.getAllDeals()
        MonthlyDeals = []
        dealsMonth = []
        d = []
        data = []
        for user in UsersDeals:
            MonthlyDeals = self.getPaymentMonths(user['deals'])
            for month in MonthlyDeals:
                for deal in user['deals']:
                    if month == deal['payment_date'][0:-3]:
                        dealsMonth.append(deal)
                d.append({"month": month, "deals": dealsMonth})
                dealsMonth = []
            data.append({"user_id" : user["userId"], "deals": d})
            d=[]
        return data

    def computeCommission(self, value: int, objective : int) -> float:
        '''
        Compute commissions depending on user objective and deals closed.

        :param self: class member functions and variables.
        :param value: total amount of money that user need to pay;
        :param objective: user's month's objective.
        :return: commission computed.
        '''

        commission = 0
        if  value <= objective:
            if value <= objective / 2:
                commission += value * 0.05
            else:
                commission += objective / 2 * 0.05
                commission += (value - objective / 2) * 0.1
        else:
            commission += objective / 2 * 0.05
            commission += objective / 2 * 0.1
            commission += (value - objective) * 0.15
        return commission

    def getObjectiveFromId(self, userId: int) -> int:
        '''
        get Objective from user's id.

        :param self: class member functions and variables.
        :param userId: id of the user.
        :return: objective of the user.
        '''
        for user in self.data["users"]:
            if userId == user['id']:
                return user['objective']
        return 0

    def computeMonthCommissions(self):
        '''
        compute commissions of user deals depending on payment date.

        :param self: class member functions and variables.
        :return: nothing.
        '''
        dealsMonth = self.getDealFromMonths()
        total_in_month = 0
        objective = 0
        commission = 0
        commissionsData = []
        dealsData = []
        jsonOutput = {}

        for user in dealsMonth:
            monthCommissions = {}
            for month in user['deals']:
                total_in_month = 0
                for deal in month['deals']:
                    total_in_month += deal["amount"]
                objective = self.getObjectiveFromId(user["user_id"])
                commission = self.computeCommission(total_in_month, objective)
                monthCommissions[month["month"]] = commission
            commissionsData.append({"user_id": user["user_id"], "commissions": monthCommissions})
        jsonOutput["commissions"] = commissionsData
        for deal in self.data["deals"]:
            objective = self.getObjectiveFromId(deal["user"])
            id = deal["id"]
            value = deal["amount"]
            commission = self.computeCommission(value, objective)
            dealsData.append({"id": id, "commission": commission})
        jsonOutput["deals"] = dealsData
        write_json_file(self.writeFile, jsonOutput, 2)

if __name__ == '__main__':
    commission = Commission("data.json")
    commission.getData("data/input.json")
    commission.computeMonthCommissions()