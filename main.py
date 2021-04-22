import os

import discord
import betting
import rewards
from functions import help_info
from functions import verify_data

token = str(os.environ['TOKEN'])
channelName = str(os.environ['CHANNELNAME'])
chennelID = int(os.environ['CHANNELID'])
betMod = str(os.environ['BETMOD'])

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #ensures the message is not from itself and it's in the right channel
    if message.author == client.user or message.channel.name != channelName:
        return

    #splits message into an list
    userMessage = message.content.split()
    user = str(message.author) + ' '


    try:
        if userMessage[0] == '!help':
            outPut = help_info(user)
            await message.channel.send('{0.author.mention}, '.format(message) + outPut)
            print(user + outPut)
    except IndexError: #if user didn't enter a message, it assigns something to the index to prevent errors
        userMessage = ['blank']

    if userMessage[0] == '!bet':
        outPut = betting.place_bet(user, userMessage, message.id)
        await message.channel.send('{0.author.mention}, '.format(message) + outPut)
        print(user + outPut)

    if userMessage[0] == '!register':
        outPut = betting.register(user)
        await message.channel.send('{0.author.mention}, '.format(message) + outPut)
        print(user + outPut)

#    if userMessage[0] == '!deregister':
#        outPut = betting.deregister(user)
#        await message.channel.send('{0.author.mention}, '.format(message) + outPut)
#        print(user + outPut)

    if userMessage[0] == '!balance':
        outPut = betting.balance(user)
        await message.channel.send('{0.author.mention}, '.format(message) + outPut)
        print(user + outPut)

    if userMessage[0] == '!current':
        outPut = betting.current_bets(user)
        await message.channel.send('{0.author.mention}, '.format(message) + outPut)
        print(user + outPut)

    if userMessage[0] == '!bonus':
        outPut = betting.daily_bonus(user)
        await message.channel.send('{0.author.mention}, '.format(message) + outPut)
        print(user + outPut)

    if userMessage[0] == '!shop':
        outPut = rewards.list_all()
        await message.channel.send('{0.author.mention}, '.format(message) + outPut)
        print(user + outPut)

    if userMessage[0] == '!cashin':
        outPut = rewards.cash_in(user, userMessage)
        await message.channel.send('{0.author.mention}, '.format(message) + outPut)
        print(user + outPut)


@client.event
async def on_reaction_add(reaction, user):
    #ensures the message is not from itself and it's in the right channel
    if reaction.message.author == client.user or reaction.message.channel.name != channelName:
        return
    
    #ensures that the user is a moderator by their group
    roleList = []
    for role in user.roles:
        roleList.append(str(role))
    if betMod not in roleList:
        return

    #calls the appropriate function based on the emoji sent by the mod
    if reaction.emoji == '👍':
        outPut = betting.bet_won(reaction.message.id)
        await client.get_channel(chennelID).send('{0.author.mention}, '.format(reaction.message) + outPut)
        print(outPut)

    elif reaction.emoji == '👎':
        outPut = betting.bet_loss(reaction.message.id)
        await client.get_channel(chennelID).send('{0.author.mention}, '.format(reaction.message) + outPut)
        print(outPut)


if __name__ == '__main__':
    verify_data()
    client.run(token)
