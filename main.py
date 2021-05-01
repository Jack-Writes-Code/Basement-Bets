import os

from functions import *
import discord
import betting
import rewards

# get variables from docker/OS if able. Otherwise declare in python
try:
    token = str(os.environ['TOKEN'])
    channelID = int(os.environ['CHANNELID'])
    betMod = int(os.environ['BETMOD'])
except KeyError:
    token = 'Your bot key here'
    channelID = 'Your channelID for the bot to monitor'
    betMod = 'The id of the role for your betmods'

client = discord.Client()

# datetime object containing current date and time
dateTime = get_dateTime()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #ensures the message is not from itself and it's in the right channel
    if message.author == client.user or message.channel.id != channelID:
        return

    user = str(message.author)
    userID = str(message.author.id)

    #splits message into an list
    userMessage = message.content.split()

    try:
        if userMessage[0] == '!help':
            outPut = help_info()
            await message.channel.send(f"{message.author.mention}, {outPut}")
            print(dateTime, user, outPut)
    except IndexError: #if user didn't enter a message, it assigns something to the index to prevent errors
        userMessage = ['blank']

    if userMessage[0] == '!register':
        outPut = register(userID, user)
        await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)

    if userMessage[0] == '!bet':
        outPut = betting.place_bet(userID, userMessage, message.id)
        sent_message = await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)
        updateRecord(LIVEBETS, message.id, sent_message.id)

    if userMessage[0] == '!challenge':
        outPut = betting.challenge(userID, userMessage, message.id)
        sent_message = await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)
        try:
            updateRecord(PENDINGCHALLENGES, message.id, sent_message.id)
        except KeyError:
            pass

    if userMessage[0] == '!gamble':
        outPut = betting.gamble(userID, userMessage)
        await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)


    if userMessage[0] == '!balance':
        outPut = balance(userID)
        await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)

    if userMessage[0] == '!current':
        outPut = betting.current_bets(userID)
        await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)

    if userMessage[0] == '!bonus':
        outPut = betting.daily_bonus(userID)
        await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)

    if userMessage[0] == '!shop':
        outPut = rewards.list_all()
        await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)

    if userMessage[0] == '!cashin':
        outPut = rewards.cash_in(userID, userMessage)
        await message.channel.send(f"{message.author.mention}, {outPut}")
        print(dateTime, user, outPut)

@client.event
async def on_reaction_add(reaction, user):
    #ensures the message is not from itself and it's in the right channel
    if reaction.message.channel.id != channelID:
        return

    #formats data for current bets and challenges
    betData = load_data(LIVEBETS)
    betList = []
    for bet in betData:
        betList.append(bet)

    challengeData = load_data(PENDINGCHALLENGES)
    challengeList = []
    for challenge in challengeData:
        challengeList.append(challenge)

    activeChallengeData = load_data(ACTIVECHALLENGES)
    activeChallengeList = []
    for activeChallenge in activeChallengeData:
        activeChallengeList.append(activeChallenge)

    roleList = []
    for role in user.roles:
        roleList.append(role.id)

    #detects reactions on pending challenges
    if str(reaction.message.id) in challengeList and user.id == int(challengeData[str(reaction.message.id)]["Challenged"]):#fix this bit
        if reaction.emoji == '👍':
            outPut = betting.challenge_accepted(reaction.message.id, user.id)
            sent_message = await client.get_channel(channelID).send(outPut)
            print(dateTime, outPut)
            updateRecord(ACTIVECHALLENGES, reaction.message.id, sent_message.id)

        elif reaction.emoji == '👎':
            outPut = betting.challenge_declined(reaction.message.id, user.id)
            await client.get_channel(channelID).send(outPut)
            print(dateTime, outPut)


    # when the person who wins likes the message
    elif str(reaction.message.id) in activeChallengeList:
        if int(user.id) == int(activeChallengeData[str(reaction.message.id)]["Challenger"]):
            outPut = betting.challengeWinner(str(reaction.message.id), activeChallengeData[str(reaction.message.id)]["Challenger"], activeChallengeData[str(reaction.message.id)]["Challenged"])
            await client.get_channel(channelID).send(outPut)
            print(dateTime, outPut)

        elif int(user.id) == int(activeChallengeData[str(reaction.message.id)]["Challenged"]):
            outPut = betting.challengeWinner(str(reaction.message.id), activeChallengeData[str(reaction.message.id)]["Challenged"], activeChallengeData[str(reaction.message.id)]["Challenger"])
            await client.get_channel(channelID).send(outPut)
            print(dateTime, outPut)


    #detects reactions on live bets
    elif str(reaction.message.id) in betList and betMod in roleList:
        if reaction.emoji == '👍':
            outPut = betting.bet_won(reaction.message.id)
            await client.get_channel(channelID).send(outPut)
            print(dateTime, outPut)

        elif reaction.emoji == '👎':
            outPut = betting.bet_loss(reaction.message.id)
            await client.get_channel(channelID).send(outPut)
            print(dateTime, outPut)









if __name__ == '__main__':
    verify_data()
    client.run(token)