import os
import time
import random

from dotenv import load_dotenv

from multifunctional_module import create_folder_safely
from multifunctional_module import get_files_paths
from multifunctional_module import find_system_files
from multifunctional_module import publish_content


def define_publication_interval(interval_hours):
	try:
		return float(interval_hours) * 3600
	except:
		return 4 * 3600


def main():
	load_dotenv()
	token = os.environ["TELEGRAM_TOKEN"]
	chat_id = os.environ["TELEGRAM_CHAT_ID"]
	interval = os.getenv("PUBLICATION_INTERVAL", default="")
	duration_sec = define_publication_interval(interval)
	images_folder = create_folder_safely()
	paths = get_files_paths(images_folder)
	while paths:
		for path in paths:
			if not find_system_files(path):
				publish_content(token, chat_id, path)
				time.sleep(duration_sec)
		random.shuffle(paths)
	print("Изображений не найдено.")


if __name__ == "__main__":
	main()
