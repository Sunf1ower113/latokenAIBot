import asyncio
from config import Config
from bot_config import BotConfig
from aiogram import Bot, Dispatcher


class LatokenAIBot:
    def __init__(self, _bot_config: BotConfig):
        self.config = bot_config

    async def run(self):
        """Запуск бота."""
        await self.config.dp.start_polling(self.config.bot)


if __name__ == '__main__':
    config = Config()

    bot_config = BotConfig(config)

    bot = LatokenAIBot(bot_config)

    asyncio.run(bot.run())
