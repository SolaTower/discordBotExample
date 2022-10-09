import logging

from DiscordBots.commands.channel import join, leave
from DiscordBots.commands.youtube import YoutubePlayer


__NAME__ = "BipBoop"

# LOGGING
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)-8s] [%(filename)s:%(funcName)s]: %(message)s",
    "%Y-%m-%d %H:%M:%S"
)
logging.basicConfig(format=    "[%(asctime)s] [%(levelname)-8s] [%(filename)s:%(funcName)s]: %(message)s",
level=logging.INFO)
logger = logging.getLogger(__NAME__)
# logger.setLevel(logging.INFO)
# sh = logging.StreamHandler()
# sh.setLevel(logging.INFO)
# sh.setFormatter(formatter)
# logger.addHandler(sh)

bot_command_list = [
    join,
    leave
]

bot_command_cog_list = [
    YoutubePlayer
]
