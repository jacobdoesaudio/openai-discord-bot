Hard fork of  AlexisTM /gpt3-discord-bot to remove all AI21 integration as well as add features not possible with original codebase


OpenAI Discord bot
==================

This is an OpenAI discord bot replying as Kirby.

Environment keys:
- OPENAI_KEY
- DISCORD_BOT_TOKEN
- DISCORD_BOT_NAME

Commands
=============

- `Kirby are you there?`: Replies yes if the server runs
- `Kirby enable`: Allow Kirby god to randomly jump into conversations (15% chance of reply)
    - `Kirby disable`: Disable the Kirby mode of the channel 
- `Kirby god: `: Answers as a Kirby god. 
    - Remembers the 5 last prompts & answers
    - Clean the memory with `Kirby clean`

Installation
==========

```bash
git clone https://github.com/jacobdoesaudio/openai-discord-bot
cd openai-discord-bot

python3 -m pip install -r requirements.txt --user

export OPENAI_KEY="someothertoken"
export DISCORD_BOT_TOKEN="sometoken" 
export DISCORD_BOT_NAME="triggerword"

python3 main.py
```


To run inside docker use:
```bash
docker build -t openai-discord-bot .
```

```bash
docker run -e OPENAI_KEY='APIKey' -e DISCORD_BOT_TOKEN='DiscordKey' -e DISCORD_BOT_NAME="triggerword" openai-discord-bot
```


Notes: 
- You can directly speak to the bot for a direct chat to Kirby
- The 5 message memory is over the same channel. I will eventually add the user name in the memory for more coherence.


Technical help on how to make a Discord bot:
==================

Create a bot application: https://discordpy.readthedocs.io/en/stable/discord.html

Configure intents for your bot: https://discordpy.readthedocs.io/en/stable/intents.html

In the oauth section of discord dev portal, make a link to allow your bot to join your server such as:

https://discord.com/api/oauth2/authorize?client_id=APPID&permissions=2215115840&scope=bot

In this case, we only need the bot scope and READ/WRITE messages permissions/