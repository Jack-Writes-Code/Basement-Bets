import json
import datetime

ACCOUNTS = 'data/accounts.json'
LIVEBETS = 'data/live_bets.json'
BETTINGHISTORY = 'data/betting_history.json'
REWARDS = 'data/rewards.json'

def verify_data():
    dataList = [ACCOUNTS, LIVEBETS, BETTINGHISTORY, REWARDS]
    for data in dataList:
        try:
            with open(data) as dataFile:
                print(f'{data} loaded.')
                pass
        except FileNotFoundError:
            jsonData = {}
            with open(data, 'w') as dataFile:
                json.dump(jsonData, dataFile, indent=4)
            print(f'{data} not found. Created new file.')

def load_data(targetLocation):
    try:
        with open(targetLocation) as dataFile:
            data = json.load(dataFile)
            return(data)
    except FileNotFoundError:
        print(f"Could not load {targetLocation}")
        verify_data()
        data = {}
        return(data)

def save_data(targetLocation, data):
    with open(targetLocation, 'w') as dataFile:
        json.dump(data, dataFile, indent=4)

def get_date():
    currentDate = []
    dateValue = datetime.datetime.now()
    currentDate.append(dateValue.strftime("%y"))
    currentDate.append(dateValue.strftime("%m"))
    currentDate.append(dateValue.strftime("%d"))
    currentDate = ''.join(currentDate)
    return(int(currentDate))

def help_info(userName):
    return(f"""
    
Here's what you can do:

!register
!bet [amount] [criteria/what you are betting to happen]
!balance (dispays current balance)
!current (to show current outstanding bets)
!bonus (gives you a daily bonus of between 1-100BB coins!)
!shop (to see what's available for purchase)
!cashin [item number as per list in !shop] (purchase your chosen reward!)

Upon placing a bet, you must then follow it up by replying to your original message where you placed the bet, with proof that it was completed. I.E a screenshot. A Bet-Mod will then 'react' to the message to confirm whether it was a success or failure!

Anyone who signs up using !register, agrees that if a reward is redeemed by another member while you're partied up- you will honour it and do what they've paid for!

In the spirit of keeping it fun, please don't submit intentionally bias bets, or bets that aren't yes/no. Try keep it competitive with some real risk!
""")

def register_check(userName):
    accountData = load_data(ACCOUNTS)
    if userName not in accountData:
        return(True)
    return(False)