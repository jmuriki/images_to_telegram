import os
import time
import random

from dotenv import load_dotenv

from multifunctional_module import create_folder_safely
from multifunctional_module import get_paths
from multifunctional_module import publish_content


def define_publication_interval(interval_hours=None):
	if interval_hours is None:
		return 4 * 3600
	else:
		return int(interval_hours * 3600)


def main():
	load_dotenv()
	token = os.environ["TELEGRAM_TOKEN"]
	chat_id = os.environ["TELEGRAM_CHAT_ID"]
	try:
		duration_sec = define_publication_interval(os.environ["PUBLICATION_INTERVAL"])
	except KeyError:
		duration_sec = define_publication_interval()
	images_folder = create_folder_safely()
	paths = get_paths(images_folder)
	while paths:
		for path in paths:
			publish_content(token, chat_id, path)
			time.sleep(duration_sec)
		random.shuffle(paths)
	print("Изображений не найдено.")


if __name__ == "__main__":
	main()
