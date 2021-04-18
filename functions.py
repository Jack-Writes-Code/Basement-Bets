import json
import datetime

ACCOUNTS = 'data/accounts.json'
LIVEBETS = 'data/live_bets.json'
BETTINGHISTORY = 'data/betting_history.json'
REWARDS = 'data/rewards.json'

def load_data(targetLocation):
    try:
        with open(targetLocation) as dataFile:
            data = json.load(dataFile)
            return(data)
    except FileNotFoundError:
        print(f"Could not load {targetLocation}")
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
!bonus (gives you a daily bonus of between 1-100 points!)
!shop (to see what's available for purchase)
!cashin [item number as per list in !shop] (purchase your chosen reward!)

Upon placing a bet, you must then follow it up by replying to your original message where you placed the bet, with proof that it was completed. I.E a screenshot. A Bet-Mod will then 'react' to the message to confirm whether it was a success or failure!
""")

def register_check(userName):
    accountData = load_data(ACCOUNTS)
    if userName not in accountData:
        return(True)
    return(False)