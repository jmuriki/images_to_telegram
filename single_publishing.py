import os
import random

from dotenv import load_dotenv

from multifunctional_module import create_parser
from multifunctional_module import create_folder_safely
from multifunctional_module import get_paths
from multifunctional_module import publish_content


def main():
	load_dotenv()
	token = os.environ["TELEGRAM_TOKEN"]
	chat_id = os.environ["TELEGRAM_CHAT_ID"]
	path = create_parser("--path").parse_args().path
	images_folder = create_folder_safely()
	paths = get_paths(images_folder)
	if not path and not paths:
		print("Изображений не найдено.")
	elif not path and paths:
		path = random.choice(paths)
	if path:
		publish_content(token, chat_id, path)

if __name__ == "__main__":
	main()
