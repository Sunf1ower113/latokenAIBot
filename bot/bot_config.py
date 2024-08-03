import logging
import openai
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command
from config import Config


class MyStates(StatesGroup):
    WAITING_FOR_MESSAGE = State()


class BotConfig:
    def __init__(self, config: Config):
        self.bot_token = config.get_bot_token()
        self.openai_api_key = config.get_openai_api_key()
        self.bot = Bot(token=self.bot_token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.setup_handlers()

        openai.api_key = self.openai_api_key

    def setup_handlers(self):
        self.dp.message.register(self.start, Command(commands=['start']))
        self.dp.message.register(self.handle_message)

    async def start(self, message: Message, state: FSMContext):
        await message.answer("Привет! Я бот, готовый помочь. Напиши мне что-нибудь.")
        await state.set_state(MyStates.WAITING_FOR_MESSAGE)

    async def handle_message(self, message: Message, state: FSMContext):
        user_message = message.text
        response = await self.get_openai_response(user_message)
        await message.answer(response)
        await state.clear()

    async def get_openai_response(self, user_message: str) -> str:
        """Получение ответа от OpenAI Assistant."""
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",  # Используйте модель, которая вам нужна
                prompt=user_message,
                max_tokens=150
            )
            return response.choices[0].text.strip()
        except Exception as e:
            logging.error(f"Error while calling OpenAI API: {e}")
            return "Произошла ошибка при обработке вашего запроса."
