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


def choose_path(paths, published_paths):
	for path in paths:
		if path not in published_paths:
			return path
	if all(path in published_paths for path in paths):
		random.shuffle(published_paths)
		return published_paths[0]


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
	published_paths = []
	while paths:
		path = choose_path(paths, published_paths)
		publish_content(token, chat_id, path)
		if path not in published_paths:
			published_paths.append(path)
		time.sleep(duration_sec)
	print("Изображений не найдено.")


if __name__ == "__main__":
	main()
