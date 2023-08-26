# orbbot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python-Versions](https://img.shields.io/badge/python-3.8-blue)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/rvalien/orbbot/master/LICENSE)
[![Discord.py-Version](https://img.shields.io/badge/discord.py-1.7-blue)](https://pypi.org/project/discord.py/)  
<img src="orbb.png" width="100">

### description

lil bot for lil discord [QC](https://quake.bethesda.net/en) channel
---

### usage

Orbb can help:  
`map`      🗺️ Choose random map.
`profile` Show quake profile link `profile some_name`  
![](./vote_exmpl.png)
`spec`    Bot send vote message with question like: `Who want to play now?` If player, that set positive reaction, more
than 8, bot choose random spectators.  
`teams`    Shuffle members of voice channel to 2 teams and spectators.  
`vote`     Shuffle members who set positive reaction to 2 teams and spectators.  
`role`     Show your roles & link to message where you can add/remove roles.  
`bday`     Show happy birthday users.
`pzdc`     OMG mode! Random team and character. Prepare to suffer.  
`help`     Shows this message and more info for commands.  
`poll`     Simple poll with only 2 reactions (👍, 👎).  
`roll`     🎲 roll dice and set result as reaction on your command. Return number from 1 to 6.  
`random`   Shuffle to 2 teams items from message input (comma separated).  
You don't need to input items again if they steal same, just type `random` without arguments.
`deadline` Show deadline date for book club. To set the date use `!deadline YYYY-MM-DD`  
![](./deadline.PNG)  
`order`    Shuffle members of voice channel




|emoji| meaning                  |valid reaction|  
|-----|--------------------------|--------------|  
|✅   |positive reaction          |yes           |   
|❌   | negative reaction         |yes           |  
|🔟   | 10 seconds until vote ends|no (vote info)|  
|5️⃣   | 5 seconds until vote ends |no (vote info)|  
|🛑   | voting is over            |no (vote info)|   



---

### setup

To run this bot, you need to set environment variables:  
`TOKEN` - [discord](https://discord.com/developers/docs/intro) bot token  
`TENSOR_API_KEY`- [gifapi](https://tenor.com/gifapi/documentation) token  
`PREFIX` - Command prefix to use.

---

### deploy

[Configure your bot here](https://discord.com/developers/applications/)  

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/rvalien/orbbot)  
[Invite link](https://discordapp.com/oauth2/authorize?&client_id=757854688518602773&scope=bot&permissions=1275591744)  
Wanna new features? [Create an issue](https://github.com/rvalien/orbbot/issues) on this repo.  
