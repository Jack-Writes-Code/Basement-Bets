# Basement-Bets 1.2 (Pickpocket update now live)
# Built and maintained by JackMWhit

Basement-Bets is a discord bot coded in Python that allows server users to place bets and win points. The users can then redeem rewards and anyone who is a part of the betting game can take part in fun challenges!

Our original deployment for this is intended so we can have fun spontaniously choosing eachother's characters or roles in games for some fun.

In order to deploy, please be sure to place your token for your bot, the channel id for your bet-channel, and the role id for your bet-moderators into the top declarations of Main.py

If you're using docker:
You must declare the ENV variables on the Dockerfile. The variable names are: 'TOKEN', 'CHANNELID', 'BETMOD'.
Finally, please be sure to mount the volume at boot with '-v your-location:/app/data' when running the container. This allows you to not lose progress when rebooting the bot.

In order to approve bets as won or lost, you'll need a to assign users to your specified role. They can then use the :thumbs-up: or :thumbs-down: reactions on the bot response message to declare it as won or lost.


Enjoy! Any issues, please feel free to submit a pull request.
