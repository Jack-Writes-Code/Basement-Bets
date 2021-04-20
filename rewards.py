from functions import *


def list_all():
    rewardData = load_data(REWARDS)

    #creates lists for the rewardData
    name = []
    for reward in rewardData:
        name.append(reward)
    fullList = ["""Here are the following items available for purchase:
"""]
    for i in range(len(name)):
        fullList.append(f"""{i}: {name[i]}. Cost: {int(rewardData[name[i]]["cost"])}BB Coins. {rewardData[name[i]]["description"]}.
""")
    sentence = ""
    for item in fullList:
        sentence += item
    sentence = sentence[:-1] #remove's final return line from string
    return(sentence)


def cash_in(userName, userMessage):
    if register_check(userName):
        return("You are not registered, so you cannot make any purchases.")

    # remove the cashin keyword
    userMessage = userMessage[1:]

    # set the input as int, or return error if not int
    try:
        choiceOfPurchase = int(userMessage[0])
    except TypeError:
        return("Please format your purchase as '!cashin [id of item as seen in !shop list]'")

    rewardData = load_data(REWARDS)
    accountData = load_data(ACCOUNTS)

    name = []
    for reward in rewardData:
        name.append(reward)

    if choiceOfPurchase > len(name):
        return("Selection out of range. Please format your purchase as '!cashin [id of item as seen in !shop list]'")

    if accountData[userName]["balance"] < rewardData[name[choiceOfPurchase]]["cost"]:
        return(f"Sorry. You do not currently have enough funds for this purchase. Cost of item is {int(rewardData[name[choiceOfPurchase]]['cost'])}, and your current balance is {accountData[userName]['balance']}.")

    accountData[userName]["balance"] -= rewardData[name[choiceOfPurchase]]["cost"]
    accountData[userName]["total purchases"] += 1

    rewardData[name[choiceOfPurchase]]["cost"] *= 1.1
    rewardData[name[choiceOfPurchase]]["purchase count"] += 1

    save_data(ACCOUNTS, accountData)
    save_data(REWARDS, rewardData)

    return(f"Congrats! You have purchased: '{name[choiceOfPurchase]}'. The following is now in effect: '{rewardData[name[choiceOfPurchase]]['description']}'.")


if __name__ == '__main__':
    outPut = list_all()
    #outPut = cash_in("Jack", ["!cash_in", "2"])
    print(outPut)