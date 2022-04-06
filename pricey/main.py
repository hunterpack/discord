import os

from init_logging import initialize_logging
from fetch_data import fetch_price, check_map
from discord.ext import commands


TOKEN = os.getenv("DISCORD_TOKEN")


def main():

    bot = commands.Bot(command_prefix="!")

    @bot.event
    async def on_ready():
        logger.info(f"{bot.user.name} has connected to Discord!")

    @bot.command(name="price")
    async def get_price(ctx, symbol):
        try:
            id_map = check_map(symbol.upper())

            if len(id_map) > 1:
                options = {}
                for ticker in id_map:
                    options[ticker["name"]] = ticker["id"]

                await ctx.send(
                    f"Please choose one of the following options: {', '.join(options.keys())}"
                )

                message_response = await bot.wait_for(
                    "message", check=lambda m: m.author == ctx.author
                )

                token_name = message_response.content

                options = {k.lower(): v for k, v in options.items()}
                ticker_id = str(options[token_name.lower()])

                response = fetch_price(id=ticker_id)
                await ctx.send(f"{token_name}'s current price is ${response}")

            else:
                ticker = symbol.upper()
                response = fetch_price(symbol=ticker)
                await ctx.send(f"{ticker}'s current price is ${response}")

        except Exception as e:
            logger.info(f"Unable to retrieve data for {symbol}")
            logger.info(f"Error: {e} not a valid symbol")
            await ctx.send(f"Unable to retrieve data for {symbol}")

    bot.run(TOKEN)


if __name__ == "__main__":
    logger = initialize_logging()
    main()
