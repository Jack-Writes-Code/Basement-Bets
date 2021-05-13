from functions import *
import random

def steal(userID, userMessage):
    #check if user registered
    if register_check(userID):
        return("You are not registered, so you can't steal from others yet.")

    #check message only contains 2 words (keyword then username)
    if len(userMessage) > 2:
        return("Too many arguments given. The syntax is: '!pickpocket [@username]'")

    #ID of the user being challenged
    try:
        targetUser = userMessage[1][3:-1]
    except IndexError:
        return("Please reformat your pickpocket. The syntax is: '!pickpocket [@user]'")

    #check target is registered and that it's not you
    if register_check(targetUser):
        return("The person you're trying to steal from isn't registered for Basement Bets.")
    if userID == targetUser:
        return("You can't steal from yourself.")


    #load data
    accountData = load_data(ACCOUNTS)

    #ensure they haven't already done it today
    if accountData[userID]["last pickpocket"] >= get_date():
        return("You have tried to pickpocket today. Come back tomorrow!")

    #make sure they can afford the gamble
    if accountData[targetUser]["balance"] < 5:
        return("Your target is too poor to pickpocketed. Try steal from someone richer!")


    accountData[userID]["last pickpocket"] = get_date()

    number = random.randrange(0,25)+1
    if number == 1:
        amount = round(accountData[targetUser]["balance"] * 0.1)
        accountData[targetUser]["balance"] -= int(amount)
        accountData[userID]["balance"] += int(amount)
        output = (f"SUCCESS! You steal {int(amount)} from <@{targetUser}>! POG")
    else:
        output = ("You failed your pickpocket! Try again tomorrow.")

    save_data(ACCOUNTS, accountData)
    return(output)