import os

from fetch_data import fetch_data, check_map
from discord.ext import commands

bot = commands.Bot(command_prefix='!')


def run(token):
    bot.run(token)


def main():
    TOKEN = os.getenv('DISCORD_TOKEN')

    @bot.event
    async def on_ready():
        print(f'{bot.user.name} has connected to Discord!')

    @bot.command(name='price')
    async def get_price(ctx, symbol):
        id_map = check_map(symbol.upper())

        if len(id_map.data) > 1:
            options = []
            for ticker in id_map.data:
                options.append(ticker["name"])
            await ctx.send(f"Please choose one of the following options: {', '.join(options)}")
        else:
            ticker = symbol.upper()

        response = fetch_data(ticker)

        await ctx.send(f"{ticker}'s current price is ${response}")

    run(TOKEN)


if __name__ == '__main__':
    main()
