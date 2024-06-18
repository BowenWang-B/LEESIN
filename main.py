import os
from dotenv import load_dotenv

load_dotenv()
import discord
from discord import app_commands
from discord.ext import commands
from firebase import db


def is_core_member(interaction: discord.Interaction) -> bool:
    user = interaction.user
    if isinstance(user, discord.Member):
        return discord.utils.get(user.roles, id=int(os.getenv("CORE_MEMBER_ROLE_ID")))
    return False


def run():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user}")
        guild_id = discord.Object(os.getenv("GUILD_ID"))
        bot.tree.copy_global_to(guild=guild_id)
        await bot.tree.sync(guild=guild_id)

    @bot.tree.command(description="查看所有账号信息")
    @app_commands.check(is_core_member)
    async def list(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        accounts = db.collection("accounts").get()
        embeds = []
        chunked_accounts = []
        chunk_size = 24

        for i in range(0, len(accounts), chunk_size):
            chunked_accounts.append(accounts[i : i + chunk_size])

        for chunk in chunked_accounts:
            embed = discord.Embed(
                title="Account Information",
                description="List of accounts with details",
                color=discord.Color.blue(),
            )
            for index, account in enumerate(chunk):
                account = account.to_dict()
                embed.add_field(
                    name=account["summonerName"],
                    value=f"账号: {account['username']}\n密码: {account['password']}",
                    inline=True,
                )
                if index % 2 == 1:
                    embed.add_field(name="\u200b", value="\u200b")

            embeds.append(embed)

        for embed in embeds:
            await interaction.followup.send(embed=embed, ephemeral=True)

    @list.error
    async def list_error(interaction: discord.Interaction, error):
        await interaction.response.send_message("爬")

    bot.run(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == "__main__":
    run()
