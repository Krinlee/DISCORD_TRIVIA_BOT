import discord, os, random, asyncio, datetime
from discord.ext import commands, tasks
from Trivia_List import *
from dotenv import load_dotenv

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='%', intents = intents)



# .env parts

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
tchan = os.getenv('TEST_CHANNEL')
tchan = int(tchan)
bchan = os.getenv('BOT_CHANNEL')
bchan = int(bchan)



# This chooses which channel to target (for trivia)

target_channel_id = bchan



# Time settings

utc = datetime.timezone.utc
time = datetime.time(hour=12, minute=5)



# Test command

@bot.command()
async def test(ctx):
    await ctx.send("This is a test!")



# Getting the Bot ready

@bot.event
async def on_ready():
    print('\n{0.user} is ready for action'.format(bot))
    trivia.start()



# Trivia loop

@tasks.loop(time=time)
async def trivia():
    message_channel = bot.get_channel(target_channel_id)
    try:
        f = open('question.txt', 'r')
        o_question = f.read()
        f.close()
        f = open('answer.txt', 'r')
        o_answer = f.read()
        f.close()
        await message_channel.send(f"""@here Yesterday's question was:
        
         ¯\_(ツ)_/¯  {o_question}  ¯\_(ツ)_/¯""")
        await message_channel.send(f"""The answer is		(っ ͡ ͡º - ͡ ͡º ς)		 -> {o_answer} <-
	
	(人❛ᴗ❛)♪тнайк　чоц♪(❛ᴗ❛*人)""")
        await asyncio.sleep(10)
        pick = trivia_List[random.randint(0, 400)]
        question = pick[0]
        answer = pick[1]
        f = open('question.txt', 'w')
        f.write(f"{question}")
        f.close()
        f = open('answer.txt', 'w')
        f.write(f"{answer}")
        f.close
    except:
        pick = trivia_List[random.randint(0, 400)]
        question = pick[0]
        answer = pick[1]
        f = open('question.txt', 'w')
        f.write(f"{question}")
        f.close()
        f = open('answer.txt', 'w')
        f.write(f"{answer}")
        f.close
    print(f"Trivia question --> {question} <-- posted to {message_channel}  --  The answer is -> {answer}")
    await message_channel.send("""@everyone 
    
    As always, post your answers to the trivia in the trivia-answers channel.

    (っ'ヮ'c)	The answer will be posted here on the next day before the next trivia question.""")
    await asyncio.sleep(3)
    await message_channel.send(f"""🧠	🧠	-> {question} <-	🧠	🧠
    
    (∩｀-´)⊃━☆ﾟ.*･｡ﾟ""")


@trivia.before_loop
async def before_trivia():
    print("\n\nTrivia is good to go!")
    await bot.wait_until_ready()



# Runs the Bot

try:
    bot.run(TOKEN)
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests")
    else:
        raise e
