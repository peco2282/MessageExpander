# Message Expander

## example
### message

![message](https://gyazo.com/aa8fe1fc884b79ed1e0488747898f923.png)

### attachment
![attachment](https://gyazo.com/cb811c7ca4bcb1ed9a299bbc9d43c9fb.png)

### embed
![embed](https://gyazo.com/dd0035964d3bed5d06be626a33300ac7.png)

## Setting...

```shell
$ pip install -U dispand
```

## Usage...

```python
import discord
from dispand import message_expander
from discord.ext import commands

bot = commands.Bot(
    intents=discord.Intents.all()
)

@bot.event
async def on_message(message: discord.Message):
    #　statements...
    await message_expander(bot=bot, message=message)
```

else if you use extention...

```python
import discord
from discord.ext.commands import Bot

INITIAL_EXTENTIONS = [
    ...,
    "dispand"
]


class Main(Bot):
    def __init__(self, **options):
        super().__init__(**options)

    async def on_ready(self):
        for cog in INITIAL_EXTENTIONS:
            self.load_extension(cog)

        print(self.user.id)
        print(self.user.name)
        print("--------------")


if __name__ == '__main__':
    Main(
        command_prefix=...,
        intents=discord.Intents.all(),
        help_command=...
    ).run("TOKEN")
```
