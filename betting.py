from functions import *
import random
   
def daily_bonus(userID):
    if register_check(userID):
        return("You are not registered, so you can't redeem your free, daily points")

    accountData = load_data(ACCOUNTS)

    if accountData[userID]["last bonus"] >= get_date():
        return("You have already redeemed today. Come back tomorrow!")

    accountData[userID]["last bonus"] = get_date()

    bonus = random.randrange(5,100)+1

    accountData[userID]["balance"] += bonus

    save_data(ACCOUNTS, accountData)
    return(f"Your daily bonus is: {bonus} BB Coins! This puts your current balance at {accountData[userID]['balance']}. Come back tomorrow for more!")

def place_bet(userID, userMessage, messageID):

    if register_check(userID):
        return("You are not registered, so you can't place a bet.")

    #convert the number entered into an int
    try:
        amount = int(userMessage[1])
    except ValueError:
        return("Please reformat your bet. The syntax is: '!bet [value] [criteria]'")

    if amount < 5:
        return("Sorry, minimum bet size must be 5 BB Coins.")

    if len(userMessage) < 3:
        return("Please reformat your bet. The syntax is: '!bet [value] [criteria]'")

    #removes the !bet and amout and then formats the userMessage into a string
    userMessage = ' '.join(userMessage[2:])

    #load account and current bet data
    accountData = load_data(ACCOUNTS)
    betData = load_data(LIVEBETS)

    #make sure they can afford to place the bet
    if amount > accountData[userID]["balance"]:
        return(f"Sorry, you do not have enough money in your account for this bet. Your current balance is {accountData[userID]['balance']}")

    accountData[userID]["balance"] -= amount #adjust the users account balance
    betData[messageID] = {"User": userID, "Bet amount": amount, "Criteria": userMessage} #create data for their bet
    accountData[userID]["bets placed"] += 1 #add to the total number of placed bets

    save_data(ACCOUNTS, accountData)
    save_data(LIVEBETS, betData)
    return(f'You have placed a bet of {amount} BBs on "{userMessage}". Your new remaining balance is {accountData[userID]["balance"]}. Good luck!')

def challenge(userID, userMessage, messageID):
    if register_check(userID):
        return("You are not registered, so you can't challenge others yet.")

    if len(userMessage) < 4:
        return("Message too short. Please reformat your challenge. The syntax is: '!challenge [@user] [value] [criteria]'")

    #ID of the user being challenged
    try:
        targetUser = userMessage[1][2:-1]
        if targetUser[0] == '!':
            targetUser = targetUser[1:]
    except IndexError:
        return("Please reformat your challenge. The syntax is: '!challenge [@user] [value] [criteria]'")

    if register_check(targetUser):
        return("The person you're challenging isn't registered for Basement Bets. The syntax is: '!challenge [@user] [value] [criteria]'")
    if userID == targetUser:
        return("You can't challenge yourself. Use !bet instead.")

    try:
        amount = int(userMessage[2])
    except ValueError:
        return("Please reformat your challenge. The syntax is: '!challenge [@user] [value] [criteria]'")

    #removes the !bet and amout and then formats the userMessage into a string
    userMessage = ' '.join(userMessage[3:])

    #targetUser amount userMessage
    accountData = load_data(ACCOUNTS)
    challengeData = load_data(PENDINGCHALLENGES)

    #make sure they can afford the challenge
    if amount > accountData[userID]["balance"]:
        return(f"Sorry, you do not have enough money in your account for this challenge. Your current balance is {accountData[userID]['balance']}")
    elif amount > accountData[targetUser]["balance"]:
        return(f"Sorry, they do not have enough money in their account for this challenge.Their current balance is {accountData[targetUser]['balance']}")

    #create data for the challenge
    challengeData[messageID] = {"Challenger": userID, "Challenger Name": accountData[userID]["name"], "Challenged": targetUser, "Challenged Name": accountData[targetUser]["name"], "Bet amount": amount, "Criteria": userMessage, "Accepted": "False"} #create date for challenge

    #up the numbers on the accounts for challenges issued/received
    accountData[userID]["challenges issued"] += 1
    accountData[userID]["balance"] -= amount
    accountData[targetUser]["challenges received"] += 1

    save_data(ACCOUNTS, accountData)
    save_data(PENDINGCHALLENGES, challengeData)

    return(f'You are challenging <@{targetUser}> to "{userMessage}" for {amount} BB Coins. <@{targetUser}>, please react to this message with either ???? or ???? to accept/decline!')

def current_bets(userID):
    if register_check(userID):
        return("You are not registered, so you have no outstanding bets")

    betData = load_data(LIVEBETS)

    #creates lists for the betData
    name = []
    for bet in betData:
        name.append(bet)
    #check to see if any belong to the user, and add them to a list if they do
    matches = []
    for item in name:
        if betData[item]["User"] == userID:
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

            gained = betValue*2
            accountData[betData[bet]["User"]]["balance"] += gained #add the value *2 to the users balance
            accountData[betData[bet]["User"]]["total gain"] += gained - betValue #add the value to the users total gain
            
            newBalance = accountData[betData[bet]["User"]]["balance"]
            betData.pop(bet) #remove the bet from live_bets

            save_data(ACCOUNTS, accountData)
            save_data(LIVEBETS, betData)

            #add the bet to betting history
            historyData = load_data(BETTINGHISTORY)

            historyData[messageID] = {"User": user, "Name": accountData[user]["name"], "Bet amount": betValue, "Criteria": betCriteria, "Win/Loss": "Win", "Date": get_date()}
            save_data(BETTINGHISTORY, historyData)

            return(f"<@{user}>, You have won your bet! You have gained {int(gained)} to give you a new total balance of {int(newBalance)}.")

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
            
            historyData[messageID] = {"User": user, "Name": accountData[user]["name"], "Bet amount": betValue, "Criteria": betCriteria, "Win/Loss": "Loss", "Date": get_date()}
            save_data(BETTINGHISTORY, historyData)

            return(f"<@{user}>, you have lost your bet! You have lost {betValue}, leaving your current balance at {userBalance}. Better luck next time!")

def challenge_accepted(messageID, userID):
    accountData = load_data(ACCOUNTS)
    challengeData = load_data(PENDINGCHALLENGES)
    activeChallengeData = load_data(ACTIVECHALLENGES)

    for challenge in challengeData: #for every challenge
        if challengeData[challenge]["Accepted"] == "False":
            if int(messageID) == int(challenge) and int(userID) == int(challengeData[challenge]["Challenged"]):

                #assign the challenged to variables for ease
                challenged = challengeData[challenge]["Challenged"]
                challenger = challengeData[challenge]["Challenger"]
                VALUE = challengeData[challenge]["Bet amount"]

                #incriment counters on the account and accordingly
                accountData[challenged]["challenges accepted"] += 1

                #take money from participant until challenge is settled
                accountData[challenged]["balance"] -= VALUE

                #update the challenge status
                challengeData[challenge]["Accepted"] = "True"

                activeChallengeData[int(messageID)] = challengeData[challenge]
                challengeData.pop(challenge)

                save_data(ACCOUNTS, accountData)
                save_data(PENDINGCHALLENGES, challengeData)
                save_data(ACTIVECHALLENGES, activeChallengeData)

                return(f"<@{challenger}>, <@{challenged}> has accepted your challenge! The winner of the challenge must react to this message with a '????' to earn their winnings! Good luck!")

def challenge_declined(messageID, userID):
    accountData = load_data(ACCOUNTS)
    challengeData = load_data(PENDINGCHALLENGES)
    challengeHistoryData = load_data(CHALLENGEHISTORY)

    for challenge in challengeData: #for every challenge
        if challengeData[challenge]["Accepted"] == "False":
            if int(messageID) == int(challenge) and int(userID) == int(challengeData[challenge]["Challenged"]):

                #assign the challenged to variables for ease
                challenged = challengeData[challenge]["Challenged"]
                challenger = challengeData[challenge]["Challenger"]
                amount = challengeData[challenge]["Bet amount"]

                #incriment counters on the account and accordingly
                accountData[challenged]["challenges declined"] =+ 1

                #return value to challenger
                accountData[challenger]["balance"] += int(amount)

                #save a record of what the challenge was
                challengeHistoryData[messageID] = challengeData[challenge]

                #remove the challenge from actives
                challengeData.pop(challenge)

                save_data(ACCOUNTS, accountData)
                save_data(PENDINGCHALLENGES, challengeData)
                save_data(CHALLENGEHISTORY, challengeHistoryData)

                return(f"<@{challenger}>, <@{challenged}> has declined your challenge... (Coward!)")

def challengeWinner(messageID, winnerID, loserID):
    accountData = load_data(ACCOUNTS)
    activeChallengeData = load_data(ACTIVECHALLENGES)
    historicalChallengeData = load_data(CHALLENGEHISTORY)

    VALUE = (activeChallengeData[messageID]["Bet amount"] * 2)

    #give the winner the gains
    accountData[winnerID]["challenges won"] += 1
    accountData[winnerID]["balance"] += int(VALUE)
    accountData[winnerID]["total gain"] += int(VALUE/2)

    accountData[loserID]["challenges lost"] += 1
    accountData[loserID]["total loss"] += int(VALUE/2)

    #moves challenge over to history
    historicalChallengeData[messageID] = activeChallengeData.pop(messageID)
    historicalChallengeData[messageID]["Winner ID"] = winnerID
    historicalChallengeData[messageID]["Winner Name"] = accountData[winnerID]["name"]

    save_data(ACCOUNTS, accountData)
    save_data(ACTIVECHALLENGES, activeChallengeData)
    save_data(CHALLENGEHISTORY, historicalChallengeData)

    return(f"<@{winnerID}> wins the challenge! They've gained {(VALUE)} BB Coins. <@{loserID}>, better luck next time!")

def gamble(userID, userMessage):
    if register_check(userID):
        return("You are not registered, so you can't challenge others yet.")

    #load data
    accountData = load_data(ACCOUNTS)

    #check message only contains 2 words (keyword then number)
    if len(userMessage) > 2:
        return("Too many arguments given. Please reformat your challenge. The syntax is: '!gamble [value]'")

    #ensure second word is an int
    try:
        amount = int(userMessage[1])
    except ValueError:
        return("Please reformat your challenge. The syntax is: '!gamble [value]'")
    except IndexError:
        return("Please give a value for your gamble. The syntax is: '!gamble [value]'")

    #if latest gamble was today
    if accountData[userID]["latest gamble"] == get_date():
        #and if they've gambled the max
        if accountData[userID]["gambles today"] > 9:
            return("Sorry, you've hit your maximum gambles today! Come back tomorrow.")
        #otherwise add one to the counter
        accountData[userID]["gambles today"] += 1
    #if it's the first today set the date and reset counter
    else:
        accountData[userID]["latest gamble"] = get_date()
        accountData[userID]["gambles today"] = 1

    if amount < 5:
        return("Sorry, minimum gamble is 5.")

    #make sure they can afford the gamble
    if amount > accountData[userID]["balance"]:
        return(f"Sorry, you do not have enough money in your account for this gamble. Your current balance is {accountData[userID]['balance']}")

    accountData[userID]["balance"] -= int(amount)

    number = random.randrange(1,3)

    if number == 1:
        accountData[userID]["balance"] += int(amount* 2)
        accountData[userID]["gamble winnings"] += int(amount)
        outPut = f"Congrats! You won! Your balance has been increased by {int(amount)}. Your new total balance is: {accountData[userID]['balance']}. You have {(10 - accountData[userID]['gambles today'])} gambles left today."
    else:
        accountData[userID]["gamble losings"] += int(amount)
        outPut = f"That's a loss I'm afraid. Better luck next time! Your new balance is: {accountData[userID]['balance']}. You have {(10 - accountData[userID]['gambles today'])} gambles left today."

    save_data(ACCOUNTS, accountData)
    return(outPut)

def give(userID, userMessage):
    if register_check(userID):
        return("You are not registered, so you can't give to others yet.")

    if len(userMessage) < 3:
        return("Message too short. Please reformat your donation. The syntax is: '!give [@user] [value]'")

    #ID of the user being challenged
    try:
        targetUser = userMessage[1][2:-1]
        if targetUser[0] == '!':
            targetUser = targetUser[1:]
    except IndexError:
        return("Please reformat your donation. The syntax is: '!give [@user] [value]'")

    if register_check(targetUser):
        return("The person you're giving to isn't registered for Basement Bets.")
    if userID == targetUser:
        return("You can't give to yourself.")

    try:
        amount = int(userMessage[2])
    except ValueError:
        return("Please reformat your donation. The syntax is: '!give [@user] [value]'")

    accountData = load_data(ACCOUNTS)

    if amount < 5:
        return("Minimum amount that can be given is 5 BB coin.")

    #make sure they can afford the challenge
    if amount > accountData[userID]["balance"]:
        return(f"Sorry, you do not have enough money in your account for this donation. Your current balance is {accountData[userID]['balance']}")

    #up the numbers on the accounts for challenges issued/received
    accountData[userID]["balance"] -= int(amount)
    accountData[targetUser]["balance"] += int(amount)

    #trying to fix an error where donor is left with a float
    accountData[userID]["balance"] = int(accountData[userID]["balance"])


    save_data(ACCOUNTS, accountData)

    return(f'You have given <@{targetUser}> {amount} BB Coins! Their new balance is {accountData[targetUser]["balance"]}, and yours is {accountData[userID]["balance"]}.')