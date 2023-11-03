import discord
from discord import app_commands
import os
from edt import EDT
import menu as mn
from log import Log


DISCORD_TOKEN = os.environ.get("FACBOT_TOKEN")
print(DISCORD_TOKEN)

log = Log(filename="log.log")


intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name = "edt", description = "Get specific EDT")
async def edt(int: discord.Interaction, promo: str, grp_td: str, grp_tp: str):
    EDT(promo, grp_td, grp_tp)
    await int.response.send_message(file=discord.File('images/emploi_du_temps.png'), ephemeral=True)

@tree.command(name = "menu", description = "Get specific RU menu")
async def menu(int: discord.Interaction, ru: str):
    menu = mn.screenshot(ru)
    await int.response.send_message(menu, ephemeral=True)



@client.event
async def on_ready():
    await tree.sync()
    message = "Logged in as " + client.user.name + " : " + str(client.user.id) + "\n------\n"
    log.begin(message)

client.run(DISCORD_TOKEN)
