import asyncio, discord, websockets, json, os
from threading import Thread
from discord.ext import commands

prefix = os.environ.get("PREFIX")
token = os.environ.get("TOKEN")
bot = commands.AutoShardedBot(command_prefix=prefix, case_insensitive=True)

async def connect():
    while True:
        try:
            ws = await websockets.connect("ws://127.0.0.1:9010")
            print("PY: Connected to socket")
            break
        except OSError: pass
    while True:
        msg = json.loads(await ws.recv())
        if "py" in msg["recipients"]:
            await ws.send(json.dumps({"recipients":msg["sender"], "sender":"py", "info":eval(msg["info"])}))

@bot.listen()
async def on_ready():
    print("PY: Ready!")

for command in os.listdir("commands"):
    if command.endswith(".py"):
        with open(f"commands/{command}") as f:
            exec(f.read())

Thread(target=exec, args=["asyncio.run(connect())", globals()]).start()

bot.run(token)