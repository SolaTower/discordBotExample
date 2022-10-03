import interactions
import env

bot = interactions.Client(
    token=env.DISCORD_TOKEN,
    default_scope=env.GUILD_ID,
)


@bot.command(
    options=[
        interactions.Option(
            name="text",
            description="What you want to say",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ]
)
async def test(ctx: interactions.CommandContext):
    """This is a test!"""
    await ctx.send("Hi there!")

bot.start()
