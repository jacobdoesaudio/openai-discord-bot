#!/usr/bin/env python3

import os
import discord
import ask_openai
from collections import defaultdict
import random

ask_god = ask_openai.ask_prompt

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
DISCORD_BOT_NAME = "Skrillex"

COMMAND_KIRBY = f"{DISCORD_BOT_NAME} god: "
COMMAND_ENABLE = f"{DISCORD_BOT_NAME} enable"
COMMAND_DISABLE = f"{DISCORD_BOT_NAME} disable"
COMMAND_CLEAN = f"{DISCORD_BOT_NAME} clean"
COMMAND_PRESENCE = f"{DISCORD_BOT_NAME} are you there?"

MEMORY_LIMIT = 0
JUMP_IN_HISTORY = 10
JUMP_IN_PROBABILITY_DEFAULT = 15


class AIPromptResponse:
    def __init__(self, prompt, response, author="You"):
        self.prompt = prompt
        self.resp = response.strip()
        self.author = author

    def __str__(self):
        return f"\n{self.author}: {self.prompt}\n{DISCORD_BOT_NAME}: {self.resp}\n"


class AIMemory:
    def __init__(self):
        self.req_resps = []

    def update(self, prompt, response, author="You"):
        self.req_resps.append(AIPromptResponse(prompt, response))
        if len(self.req_resps) > MEMORY_LIMIT:
            self.req_resps.pop(0)

    def clear(self):
        self.req_resps = []

    def get(self):
        result = "".join([])
        if len(self.req_resps) <= 2:
            result += str()
        else:
            for val in self.req_resps:
                result += str(val)
        return result


last_ai_request = defaultdict(AIMemory)
enabled_channels = dict()


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return

        data = message.content
        source = ""
        if type(message.channel) is discord.DMChannel:
            source = "".join(["#", message.channel.recipient.name])
        elif message.guild:
            source = "".join([message.guild.name, "#", message.channel.name])
        else:
            source = "".join(["#", message.channel.name])

        if data.startswith(COMMAND_KIRBY):
            prompt = ""
            prompt = data[len(COMMAND_KIRBY):]
            ai_prompt = f"{last_ai_request[source].get()}\nYou: {prompt}\n{DISCORD_BOT_NAME}:"
            print('Prompt: {0}'.format(ai_prompt))
            result = ask_god(ai_prompt)
            if result != "":
                last_ai_request[source].update(
                    prompt, result, message.author.name)
                await message.channel.send('{0}'.format(result))
        elif data.startswith(COMMAND_ENABLE):
            enabled_channels[hash(message.channel)
                             ] = JUMP_IN_PROBABILITY_DEFAULT
            print(f'{DISCORD_BOT_NAME} enabled for channel {message.channel}')
            await message.channel.send(f"{DISCORD_BOT_NAME} started lurking in this channel.")
        elif data.startswith(COMMAND_PRESENCE):
            await message.channel.send("Yes.")
        elif data.startswith(COMMAND_CLEAN):
            last_ai_request[source].clear()
            await message.channel.send(f"{DISCORD_BOT_NAME} just forgot all about {source}")
        elif data.startswith(COMMAND_DISABLE):
            if hash(message.channel) in enabled_channels:
                del enabled_channels[hash(message.channel)]
                await message.channel.send(f"{DISCORD_BOT_NAME} left this channel.")
            else:
                await message.channel.send(f"{DISCORD_BOT_NAME} was not even here!")
        elif f"{DISCORD_BOT_NAME}".lower() in data.lower():
            prompt = data
            ai_prompt = f"{last_ai_request[source].get()}\nYou: {prompt}\n{DISCORD_BOT_NAME}:"
            print('Prompt: {0}'.format(ai_prompt))
            result = ask_god(ai_prompt)
            if result != "":
                last_ai_request[source].update(
                    prompt, result, message.author.name)
                await message.channel.send('{0}'.format(result))
        # elif data.startswith(COMMAND_SHAKESPEARE):
        #     prompt = data[len(COMMAND_SHAKESPEARE):]
        #     result = ask_god(prompt, stopSequences=["\n\n\n"])
        #     if result != "":
        #         await message.channel.send('{0}{1}'.format(prompt, result))

        # elif data.startswith(COMMAND_MARV):
        #     prompt = ""
        #     prompt = data[len(COMMAND_MARV):]
        #     ai_prompt = MARV_PROMPT.format(prompt)
        #     print('Prompt: {0}'.format(ai_prompt))
        #     result = ask_god(ai_prompt, stopSequences=["Marv:", "You:"])
        #     if result != "":
        #         await message.channel.send('{0}'.format(result))

        elif type(message.channel) is discord.DMChannel:
            prompt = data
            ai_prompt = f"{last_ai_request[source].get()}\nYou: {data}\n{DISCORD_BOT_NAME}:"
            print('Prompt: {0}'.format(ai_prompt))
            result = ask_god(ai_prompt)
            if result != "":
                last_ai_request[source].update(
                    prompt, result, message.author.name)
                await message.channel.send('{0}'.format(result))
        else:  # Random responses
            if hash(message.channel) not in enabled_channels:
                return
            if enabled_channels[hash(message.channel)] <= random.randint(0, 99):
                return

            prompt = f"This is a conversation between {DISCORD_BOT_NAME}, god of all beings and his subjects.\n\n"
            prompt = f"\n\n{DISCORD_BOT_NAME} god: I am {DISCORD_BOT_NAME}. What can I do for you?"

            hisory = await message.channel.history(limit=10).flatten()
            # .flatten()
            for history_message in reversed(hisory):
                prompt += "\n\n" + \
                    str(history_message.author.name) + \
                    ": " + str(history_message.content)
                if history_message.author == client.user:
                    pass
            prompt += f"\n\n{DISCORD_BOT_NAME} god: "
            print(prompt)

            result = ask_god(prompt)
            if result != "":
                last_ai_request[source].update(
                    prompt, result, message.author.name)
                await message.channel.send('{0}'.format(result))


intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.guilds = True
intents.reactions = True
client = MyClient(intents=intents)
client.run(DISCORD_BOT_TOKEN)
