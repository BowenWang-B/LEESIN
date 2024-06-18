import os
from dotenv import load_dotenv

load_dotenv()
import discord
from discord.ext import commands
from firebase import db


def run():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.command()
    async def list(ctx):
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
            await ctx.send(embed=embed)

    bot.run(os.getenv("DISCORD_BOT_TOKEN"))


if __name__ == "__main__":
    run()
