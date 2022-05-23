from utils import write_json_file, open_json_file
import sys

def number_of_deals(user_id: int, deals: dict):
    '''
    Retrieve the number of deals for one user.

    :param user_id: user's id.
    :param deals: List of every deals that occured.
    :return: number of deals that user closed.
    '''

    deal_count = 0
    for deal in deals:
        if deal['user'] == user_id:
            deal_count += 1
    return deal_count

def deals_amout(user_id: int, deals: dict):
    '''
    Retrieve the total amount of the deals that the user closed.

    :param user_id: user's id.
    :param deals: List of every deals that occured.
    :return: total amount of the deals that the user closed.
    '''

    amount = 0

    for deal in deals:
        if deal['user'] == user_id:
            amount += deal['amount']
    return amount

def compute_commission(deals_num: int, total_amout: int):
    '''
    Retrieve the total amount of the deals that one user closed.

    :param user_id: user's id.
    :param deals: List of every deals that occured.
    :return: total amount of the deals that the user closed.
    '''

    commission = 0

    if deals_num == 1 or deals_num == 2:
        commission = int(total_amout * 0.1)
    elif deals_num > 2:
        commission = int(total_amout * 0.2)
    else:
        raise ValueError('no deals to compute commission')

    if total_amout > 2000:
        commission += 500
    return commission

def commission_calculator(filepath: str):
    '''
    Compute commissions for user from json file and write it in an other file.

    :param filepath: name and path of the file.
    :return: No return value.
    '''
    data = open_json_file(filepath)
    commission_dict = {'commissions': []}
    for users in data['users']:
        deals = number_of_deals(users['id'], data['deals'])
        amount = deals_amout(users['id'], data['deals'])
        commission = compute_commission(deals, amount)
        commission_dict['commissions'].append({'user_id': users['id'], 'commission': commission})
    write_json_file('data.json', commission_dict, 2)

if __name__ == '__main__':
    try:
        commission_calculator(sys.argv[1])
    except Exception as e:
        print("Error:", e)
        exit(1)