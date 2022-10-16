import os
import random

from dotenv import load_dotenv

from multifunctional_module import create_folder_safely
from multifunctional_module import get_paths
from multifunctional_module import publish_content


def main():
	load_dotenv()
	token = os.environ["TELEGRAM_TOKEN"]
	chat_id = os.environ["TELEGRAM_CHAT_ID"]
	images_folder = create_folder_safely()
	try:
		path = os.environ["PRIORITY_IMAGE_PATH"]
	except KeyError:
		path = ""
		paths = get_paths(images_folder)
		if paths:
			path = random.choice(paths)
	if path:
		publish_content(token, chat_id, path)
	else:
		print("Изображений не найдено.")


if __name__ == "__main__":
	main()
