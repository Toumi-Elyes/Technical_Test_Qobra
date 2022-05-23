const process = require('process');
const fs = require("fs");
const { exit } = require('process');

const args = process.argv;
const computeCommission = (objective, deals) => {
    /*
    Compute commissions depending on user objective and deals closed.

    :param objective: user's month's objective.
    :param deals: deal's list that the user closed.
    :return: commissions computed.
    */
    const DealsTotal = deals.map(deal => deal.amount).reduce((a, b) => a + b, 0);
    let commission = 0;

    if (DealsTotal <= objective) {
        commission += objective / 2 * 0.1;
        if (DealsTotal <= objective / 2) {
            commission += objective / 2 * 0.05;
        }
    } else {
        commission += objective / 2 * 0.05;
        commission += objective / 2 * 0.1;
        commission += (DealsTotal - objective) * 0.15;
    }
    return commission;
};

const readFile = (filepath) => {
    /*
    Read file and save the content.

    :param filepath: name and path of the file.
    :return: fileContent or undefined on failure.
    */
    try {
        const content = fs.readFileSync(filepath);
        return content.toString();
    } catch (e) {
        console.log(e);
        return undefined;
    }
};

const commissionCalculator = (filepath) => {
    /*
    Compute commissions for user from json file and write it in an other file.

    :param filepath: name and path of the file.
    :return: No return value.
    */
    const fileContent = readFile(filepath);

    if (fileContent === undefined) {
        exit(1);
    }
    const ObjectContent = JSON.parse(fileContent);
    let commissions = []
    ObjectContent.users.map(user => {
        const userDeals = ObjectContent.deals.filter(deal => deal.user === user.id);
        const commission = computeCommission(user.objective, userDeals);
        commissions.push({'user_id': user.id, commission});
    })
    fs.writeFile('./data.json', JSON.stringify({commissions}, null, 2), err => {});
};
commissionCalculator(args[2]);
