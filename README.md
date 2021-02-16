# orbbot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python-Versions](https://img.shields.io/badge/python-3.8-blue)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/rvalien/orbbot/master/LICENSE)
[![Discord.py-Version](https://img.shields.io/badge/discord.py-1.6-blue)](https://pypi.org/project/discord.py/)  
<img src="orbb.png" width="100">

### description

lil bot for lil discord [QC](https://quake.bethesda.net/en) channel
---

### usage

Orbb can help:  
`map`     🗺️ choose random map  
`profile` 😸 show quake profile link `profile some_name`  
`spec`    Bot send vote message with question like: `Who want to play now?` If player, that set positive reaction, more
than 8, bot choose random spectators.  
`team`    👨‍👩‍👧‍👦 vs 👨‍👨‍👧‍👧 shuffle members of voice channel to 2 teams and spectators  
`team anything`    👨‍👩‍👧‍👦 vs 👨‍👨‍👧‍👧 shuffle members who set positive reaction to 2 teams and spectators  
`pzdc`    OMG mode! Random team, map and character. Prepare to suffer.  
`ping` used to check if the bot is alive  
`help`    Shows this message and more info for commands.  
`poll` simple poll with only 2 reactions (👍, 👎)  

#### info:
in `pzdc` & `team anything` command use emoji vote mode.
You need to react on bot vote message.  
example:  
![](./vote_exmpl.png)


|emoji| meaning                  |valid reaction|  
|-----|--------------------------|--------------|  
|✅   |positive reaction          |yes           |   
|❌   | negative reaction         |yes           |  
|🔟   | 10 seconds until vote ends|no (vote info)|  
|5️⃣   | 5 seconds until vote ends |no (vote info)|  
|🛑   | voting is over            |no (vote info)|   



---

### setup

to run this bot, you need to set environment variables:  
`TOKEN` - [discord](https://discord.com/developers/docs/intro) bot token  
`TENSOR_API_KEY`- [gifapi](https://tenor.com/gifapi/documentation) token  
`PREFIX` - Command prefix to use

---

### deploy

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/rvalien/orbbot)

Wanna new features? [Create an issue](https://github.com/rvalien/orbbot/issues) on this repo.