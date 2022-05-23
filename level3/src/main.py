import json
from utils import write_json_file, open_json_file
import sys

class Commission:
    def __init__(self, filepath : str):
        self.writeFile = filepath
        self.data = {}

    def getData(self, filepath : str):
        self.data = open_json_file(filepath)

    def getDealsFromId(self, userId : int):
        userDeals = []
        for deal in self.data['deals']:
            if deal['user'] == userId:
                userDeals.append(deal)
        return {"userId" : userId, "deals": userDeals}

    def getAllDeals(self):
        deals = []

        for user in self.data['users']:
            deals.append(self.getDealsFromId(user['id']))
        return deals

    def getPaymentMonths(self, userDeals : dict):

        months = []
        for deal in userDeals:
            months.append(deal['payment_date'][0:-3])
        return list(dict.fromkeys(months))

    def getDealFromMonths(self):
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

    def computeCommission(self, value: int, objective : int):
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

    def getObjectiveFromId(self, userId: int):
        for user in self.data["users"]:
            if userId == user['id']:
                return user['objective']
        return 0

    def computeMonthCommissions(self):
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
    commission = Commission("new.json")
    commission.getData(sys.argv[1])
    commission.computeMonthCommissions()
    exit (0)