import os
from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()

        self.bot_token = os.getenv('BOT_TOKEN')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

    def get_bot_token(self) -> str:
        if self.bot_token is None:
            raise ValueError("BOT_TOKEN not found in environment variables.")
        return self.bot_token

    def get_openai_api_key(self) -> str:
        if self.openai_api_key is None:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")
        return self.openai_api_key
