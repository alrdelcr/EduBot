import discord
import os
import dotenv
from discord.ext import commands
import configparser
import ratemyprofessor
import json
import os.path
from Messages import help_message



botDescription="Bot"
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="?", help_command=None, description=botDescription, intents=intents)



parser = configparser.ConfigParser()
parser.read("token.ini")


@client.event
async def on_ready():
    print('EduBot is educating.')

@client.event
async def on_message(message):

    #help message
    if message.content.startswith('!help'):
        await message.channel.send(help_message)
        return

    #rate my professor information
    elif message.content.startswith('!rmp'):
        message.content = message.content[5::]
        school = (message.content.split(',')[0]).strip()
        professor = (message.content.split(',')[1]).strip()
        ratings = ratemyprofessor.get_professor_by_school_and_name(ratemyprofessor.get_school_by_name(school), professor)
        try:
            r = ("Rating:" + str(ratings.rating))
            d = ("Difficulty:" + str(ratings.difficulty))
            await message.channel.send(r)
            await message.channel.send(d)
            if ratings.rating <= 2:
                await message.channel.send("Now me personally... I would wait for next quarter")
            elif ratings.rating < 4 and ratings.rating > 2:
                await message.channel.send("They're alright, I would take the chance if you really need it")
            else:
                await message.channel.send("Beautiful...take the class")
                return
        except:
            await message.channel.send("I have no idea who that is; Try Again?")


    #todo list
    elif message.content.startswith('!td'): 
        message.content = message.content[4::]
        if (message.content[0:5].lower()) == "tasks": # check tasks: !td tasks
            if os.path.exists("tasks"):
                try:
                    with open('tasks','r') as f:
                        l = json.load(f)
                    await message.channel.send("Your tasks are: \n")
                    for task in l:
                        await message.channel.send(task + "\n")
                except:
                    await message.channel.send("You have not specified any tasks!")
                    return
        elif (message.content[0:8].lower()) == "finished": # remove a finished task from tasks: !td finished 'task'
            finished = message.content[8::].strip()
            with open('tasks','r') as f:
                l = json.load(f)
            try:
                l.remove(finished)
                with open('tasks','w') as f:
                    json.dump(l, f)
            except:
                await message.channel.send("task not in to-do list")
            if len(l) == 0:
                await message.channel.send("All tasks completed.")
        elif (message.content[0:3].lower()) == "add":
            with open('tasks','r') as f:
                l = json.load(f)
            t = (message.content.split(' ')[1])
            l.append(t)
            with open('tasks','w') as f:
                    json.dump(l, f)
        else: # input is tasks that you want completed that day: !td ...,....,...
            tasks = (message.content.split(','))
            tasks = [tasks.strip() for tasks in tasks]
            with open('tasks','w') as f:
                json.dump(tasks, f)
            await message.channel.send("Tasks specified!")
            return


    
    elif message.content.startswith('!mat'): #math help
        return
    elif message.content.startswith('!mla'): #cite source
        return
    elif message.content.startswith('!play'): #music
        return
client.run(parser.get("token","token"))