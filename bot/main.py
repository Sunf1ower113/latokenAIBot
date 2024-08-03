import asyncio
import logging

from config import Config
from bot_config import BotConfig
from resources import PROMPT, SYSTEM

logging.basicConfig(level=logging.INFO)


class LatokenAIBot:
    def __init__(self, _bot_config: BotConfig):
        self.config = bot_config
        bot_config.set_context(self.create_context())

    async def run(self):
        await self.config.dp.start_polling(self.config.bot)

    def create_context(self):
        context = [{"role": "system", "content": SYSTEM},
                   {"role": "system", "content": PROMPT}
                   ]
        return context


if __name__ == '__main__':
    config = Config()

    bot_config = BotConfig(config)

    bot = LatokenAIBot(bot_config)
    asyncio.run(bot.run())
