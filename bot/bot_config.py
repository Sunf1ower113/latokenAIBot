import logging
import openai
from openai import OpenAI
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.filters import Command
from config import Config
from openai.types.chat.completion_create_params import ResponseFormat as rs


class MyStates(StatesGroup):
    WAITING_FOR_MESSAGE = State()


class BotConfig:
    def __init__(self, config: Config):
        self.context = None
        self.bot_token = config.get_bot_token()
        self.bot = Bot(token=self.bot_token)
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.setup_handlers()
        self.client = OpenAI(api_key=config.get_openai_api_key())

    def setup_handlers(self):
        self.dp.message.register(self.start, Command(commands=['start']))
        self.dp.message.register(self.handle_message)

    def set_context(self, context: list[dict]):
        self.context = context

    async def start(self, message: Message, state: FSMContext):
        await message.answer("Привет! Приглашаю тебя зарегистрироваться на наш хакатон: "
                             "https://calendly.com/latoken-career-events/ai-hackathon.")
        await state.set_state(MyStates.WAITING_FOR_MESSAGE)

    async def handle_message(self, message: Message, state: FSMContext):
        response = await self.get_openai_response(message.text, message.from_user.first_name)
        await message.answer(response)
        await state.clear()

    async def get_openai_response(self, message: str, username: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.context + [
                    {"role": "user", "content": message},
                ],
                max_tokens=2500,
                temperature=0.7,
                frequency_penalty=1,
                presence_penalty=0,
                user=username
            )
            return response.choices[0].message.content
        except Exception as e:
            logging.error(f"Error while calling OpenAI API: {e}")
            return "Произошла ошибка при обработке вашего запроса."
