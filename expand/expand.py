import re
from typing import List, Pattern, Iterator, Match

from discord import Message, Embed, Colour, NotFound
from discord.ext.commands import Bot, Cog

message_pattern: Pattern[str] = re.compile(
    r"https://(canary.|ptb.)?discord(app)?.com/channels/(\d{18,19})/(\d{18,19})/(\d{18,19})"
)


async def get_messages(bot: Bot, message: Message) -> List[Message]:
    """It takes a message, finds all the message links in it, and returns a list of the messages that were linked

    Parameters
    ----------
    bot : Bot
        Bot - The bot object
    message : Message
        The message that was sent.

    Returns
    -------
        A list of messages

    """
    messages: List[Message] = []
    result: Iterator[Match[str]] = message_pattern.finditer(message.content)
    for r in result:
        if sum(1 for _ in r.groups()) != 5:
            print("continue")
            continue
        try:
            fetched_message: Message = await bot.get_guild(
                int(r.group(3))
            ).get_channel(
                int(r.group(4))
            ).fetch_message(
                int(r.group(5))
            )
            messages.append(fetched_message)

        except NotFound:
            pass

    return messages


def create_embed(message: Message) -> Embed:
    """It creates an embed object with the message's content, author, timestamp, and channel

    Parameters
    ----------
    message : Message
        Message - The message that you want to embed

    Returns
    -------
        A discord.py Embed object

    """
    embed: Embed = Embed(
        title="To message",
        description=message.content,
        timestamp=message.created_at,
        colour=Colour.yellow(),
        url=message.jump_url
    )
    if message.author.avatar:
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar.url
        )

    else:
        embed.set_author(
            name=message.author.name
        )
    embed.set_footer(
        text=f"channel: {message.channel.name} in {message.guild.name}"
    )

    return embed


async def message_expander(bot: Bot, message: Message) -> None:
    """It takes a message, gets all the messages in the channel, and then sends them to the channel

    Parameters
    ----------
    bot : Bot
        Bot = The bot object
    message : Message
        The message object that triggered the command.

    """
    sent_messages: List = []

    messages: List[Message] = await get_messages(
        bot=bot,
        message=message
    )

    for msg in messages:
        if msg.attachments:
            print(msg.attachments)
            for attachment in msg.attachments:
                await message.channel.send(
                    embed=Embed().set_image(
                        url=attachment.proxy_url or attachment.url or None
                    )
                )

        if msg.embeds:
            for _embed in msg.embeds:
                await message.channel.send(
                    embed=_embed
                )

        if msg.content:
            embed = create_embed(message=msg)
            await message.channel.send(embed=embed)

        else:
            pass


class Expander(Cog):
    def __init__(self, bot: Bot):
        """It initializes the cog

        Parameters
        ----------
        bot : Bot
            Bot - This is the bot that the cog is being loaded into.

        """
        self.bot = bot

    @Cog.listener()
    async def on_message(self, message: Message):
        await message_expander(bot=self.bot, message=message)


def setup(bot: Bot):
    bot.add_cog(Expander(bot=bot))
