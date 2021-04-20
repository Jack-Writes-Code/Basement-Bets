from functions import *
import random


def register(userName):
    if register_check(userName) == False:
        return("You are already registered! If you'd like to know your current balance, try '!balance'. Or, try '!help' for more options!")
    accountData = load_data(ACCOUNTS)
    accountData[userName] = {"balance": 100, "total gain": 0,"total loss": 0, "total spent": 0, "total purchases": 0, "bets placed": 0, "bets won": 0, "bets lost": 0, "last bonus": get_date()-1}
    save_data(ACCOUNTS, accountData)
    return(f"You are now signed up! Your starting balance is {accountData[userName]['balance']}!")


def deregister(userName):
    if register_check(userName):
        return("You are not registered, so you can't deregister.")
    accountData = load_data(ACCOUNTS)
    accountData.pop(userName)
    save_data(ACCOUNTS, accountData)
    return("You have deregistered from the Basement Bets games")
    

def place_bet(userName, userMessage, messageID):

    if register_check(userName):
        return("You are not registered, so you can't place a bet.")

    #convert the number entered into an int
    try:
        amount = int(userMessage[1])
    except ValueError:
        return("Please reformat your bet. The syntax is: '!bet [number] [criteria]'")

    #removes the !bet and amout and then formats the userMessage into a string
    userMessage = userMessage[2:]
    userMessage = ' '.join(userMessage) # turn the message from a list into string

    #load account and current bet data
    accountData = load_data(ACCOUNTS)
    betData = load_data(LIVEBETS)

    #make sure they can afford to place the bet
    if amount > accountData[userName]["balance"]:
        return(f"Sorry, you do not have enough money in your account for this bet. Your current balance is {accountData[userName]['balance']}")

    accountData[userName]["balance"] -= amount #adjust the users account balance
    betData[messageID] = {"User": userName, "Bet amount": amount, "Criteria": userMessage} #create data for their bet
    accountData[userName]["bets placed"] += 1 #add to the total number of placed bets

    save_data(ACCOUNTS, accountData)
    save_data(LIVEBETS, betData)
    return(f'You have placed a bet of {amount} BBs on "{userMessage}". Your new remaining balance is {accountData[userName]["balance"]}. Good luck!')


def balance(userName):
    if register_check(userName):
        return("You are not registered, so you can't check balance.")
    
    accountData = load_data(ACCOUNTS)

    userBalance = accountData[userName]["balance"]
    return(f"Your current balance is: {userBalance} BB Coins.")


def current_bets(userName):
    if register_check(userName):
        return("You are not registered, so you have no outstanding bets")

    betData = load_data(LIVEBETS)

    #creates lists for the betData
    name = []
    for bet in betData:
        name.append(bet)
    #check to see if any belong to the user, and add them to a list if they do
    matches = []
    for item in name:
        if betData[item]["User"] == userName:
            matches.append(f'''Bet of {betData[item]['Bet amount']} BBs placed for: "{betData[item]['Criteria']}".
''')
    if len(matches) == 0:
        return("You currently have no active bets.")
    #combine the list into one large string and return it
    sentence = """Here are your active bets:
"""
    for match in matches:
        sentence += match
    sentence = sentence[:-1]
    return(sentence)


def bet_won(messageID):
    accountData = load_data(ACCOUNTS)
    betData = load_data(LIVEBETS)

    for bet in betData:
        if int(messageID) == int(bet):
            user = betData[bet]["User"]
            betValue = betData[bet]["Bet amount"]
            betCriteria = betData[bet]["Criteria"]

            accountData[user]["bets won"] += 1 #incriment the accounts bet win total

            if betValue <= 300:
                gained = betValue*2
                accountData[betData[bet]["User"]]["balance"] += gained #add the value *2 to the users balance
                accountData[betData[bet]["User"]]["total gain"] += gained - betValue #add the value to the users total gain
            elif betValue <= 500:
                gained = betValue*1.8
                accountData[betData[bet]["User"]]["balance"] += gained
                accountData[betData[bet]["User"]]["total gain"] += gained - betValue
            elif betValue <= 800:
                gained = betValue*1.6
                accountData[betData[bet]["User"]]["balance"] += gained
                accountData[betData[bet]["User"]]["total gain"] += gained - betValue 
            else:
                gained = betValue*1.4
                accountData[betData[bet]["User"]]["balance"] += gained
                accountData[betData[bet]["User"]]["total gain"] += gained - betValue 

            newBalance = accountData[betData[bet]["User"]]["balance"]
            betData.pop(bet) #remove the bet from live_bets

            save_data(ACCOUNTS, accountData)
            save_data(LIVEBETS, betData)

            #add the bet to betting history
            historyData = load_data(BETTINGHISTORY)
            historyData[messageID] = {"User": user, "Bet amount": betValue, "Criteria": betCriteria, "Win/Loss": "Win", "Date": get_date()}
            save_data(BETTINGHISTORY, historyData)

            return(f"You have won your bet! You have gained {int(gained)} to give you a new total balance of {int(newBalance)}.")

def bet_loss(messageID):
    accountData = load_data(ACCOUNTS)
    betData = load_data(LIVEBETS)

    for bet in betData:
        if int(messageID) == int(bet):
            user = betData[bet]["User"]
            userBalance = accountData[betData[bet]["User"]]["balance"]
            betValue = betData[bet]["Bet amount"]
            betCriteria = betData[bet]["Criteria"]

            accountData[user]["bets lost"] += 1 #incriment the accounts bet lost total
            accountData[betData[bet]["User"]]["total loss"] += betValue #add the value to the users total loss

            betData.pop(bet) #remove the bet from live_bets.json

            save_data(ACCOUNTS, accountData)
            save_data(LIVEBETS, betData)

            #add the bet to betting history

            historyData = load_data(BETTINGHISTORY)
            historyData[messageID] = {"User": user, "Bet amount": betValue, "Criteria": betCriteria, "Win/Loss": "Loss", "Date": get_date()}
            save_data(BETTINGHISTORY, historyData)

            return(f"You have lost your bet! You have lost {betValue}, leaving your current balance at {userBalance}. Better luck next time!")

def daily_bonus(userName):
    if register_check(userName):
        return("You are not registered, so you can't redeem your free, daily points")

    accountData = load_data(ACCOUNTS)

    if accountData[userName]["last bonus"] >= get_date():
        return("You have already redeemed today. Come back tomorrow!")

    accountData[userName]["last bonus"] = get_date()

    bonus = random.randrange(0,100)+1

    accountData[userName]["balance"] += bonus

    save_data(ACCOUNTS, accountData)
    return(f"Your daily bonus is: {bonus} BB Coins! This puts your current balance at {accountData[userName]['balance']}. Come back tomorrow for more!")