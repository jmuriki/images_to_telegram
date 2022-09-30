import os
import telegram

from dotenv import load_dotenv


def main():
	load_dotenv()
	token = os.environ['TELEGRAM_TOKEN']
	chat_id = os.environ['CHAT_ID']
	bot = telegram.Bot(token=token)
	bot.send_message(text='Поехали!', chat_id=chat_id)


if __name__ == "__main__":
	main()
