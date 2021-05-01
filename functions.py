import json
from datetime import datetime

ACCOUNTS = 'data/accounts.json'
LIVEBETS = 'data/bets/live.json'
BETTINGHISTORY = 'data/bets/history.json'
REWARDS = 'data/rewards.json'
CHALLENGEHISTORY = 'data/challenges/history.json'
PENDINGCHALLENGES = 'data/challenges/pending.json'
ACTIVECHALLENGES = 'data/challenges/active.json'

def verify_data():
    dataList = [ACCOUNTS, LIVEBETS, BETTINGHISTORY, REWARDS, CHALLENGEHISTORY, PENDINGCHALLENGES, ACTIVECHALLENGES]
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

def register(userID, userName):
    if register_check(userID) == False:
        return("You are already registered! If you'd like to know your current balance, try '!balance'. Or, try '!help' for more options!")
    accountData = load_data(ACCOUNTS)
    accountData[userID] = {
        "name": userName,
        "balance": 100,
        "total gain": 0,
        "total loss": 0,
        "total spent": 0,
        "total purchases": 0,
        "bets placed": 0,
        "bets won": 0,
        "bets lost": 0,
        "challenges issued": 0,
        "challenges received": 0,
        "challenges accepted": 0,
        "challenges declined": 0,
        "challenges won": 0,
        "challenges lost": 0,
        "last bonus": get_date()-1
    }
    save_data(ACCOUNTS, accountData)
    return(f"You are now signed up! Your starting balance is {accountData[userID]['balance']}!")

def deregister(userID, userName):
    if register_check(userID):
        return("You are not registered, so you can't deregister.")
    accountData = load_data(ACCOUNTS)
    accountData.pop(userID)
    save_data(ACCOUNTS, accountData)
    return("You have deregistered from the Basement Bets games")

def balance(userID):
    if register_check(userID):
        return("You are not registered, so you can't check balance.")
    
    accountData = load_data(ACCOUNTS)

    userBalance = accountData[userID]["balance"]
    return(f"Your current balance is: {userBalance} BB Coins.")

def get_date():
    currentDate = []
    dateValue = datetime.now()
    currentDate.append(dateValue.strftime("%y"))
    currentDate.append(dateValue.strftime("%m"))
    currentDate.append(dateValue.strftime("%d"))
    currentDate = ''.join(currentDate)
    return(int(currentDate))

def get_dateTime():
    return(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

def help_info():
    return("""
    
Here's what you can do:

!register
!bet [amount] [criteria/what you are betting to happen]
!challenge [@user to challenge] [amount] [criteria/what to happen]
!gamble [amount] (a 1 in 3 chance to double your money!)
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

def updateRecord(dataLocation, oldRecord, newRecord):
    data = load_data(dataLocation)
    data[str(newRecord)] = data.pop(str(oldRecord))
    print(f'Record {str(oldRecord)} updated to {str(newRecord)}.')
    save_data(dataLocation, data)