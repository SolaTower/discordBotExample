import asyncio

from discord.ext import commands
import discord

from DiscordBots import bot_command_list, bot_command_cog_list, __NAME__, logger
import env


async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix='!', intents=intents)

    async with client:
        for bot_command in bot_command_list:
            client.add_command(bot_command)
        for bot_command_cog in bot_command_cog_list:
            await client.add_cog(bot_command_cog(client))

        logger.info(f'-----{__NAME__} is up and running-----')
        await client.start(env.DISCORD_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
