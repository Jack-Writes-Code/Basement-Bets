# Basement-Bets 1.0
# Built and maintained by JackMWhit

Basement-Bets is a discord bot coded in Python that allows server users to place bets and win points. The users can then redeem rewards and anyone who is a part of the betting game can take part in fun challenges!

Our original deployment for this is intended so we can have fun spontaniously choosing eachother's characters or roles in games for some fun games!

In order to deploy, please be sure to place your token for your bot, the channel name for your bet-channel, and the role for your bet-moderators into the top declarations of Main.py

In order to approve bets as won or lost, you'll need a to assign users to your specified role. They can then use the :thumbs-up: or :thumbs-down: reactions on the original bet-placing message to declare it as won or not.


If you're using docker:
You must declare the ENV variables on the Dockerfile. The variable names are: 'TOKEN', 'CHANNELNAME', 'BETMOD'.
Finally, please be sure to mount the volume at boot with '-v your-location:/app' when running the container. This allows you to not lose progress when rebooting the bot.

Enjoy! Any issues, please feel free to submit a pull request.