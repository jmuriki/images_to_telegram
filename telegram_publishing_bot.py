import os
import time
import telegram
import random
import requests

from dotenv import load_dotenv
from pathlib import Path

from multifunctional_module import scout_directories
from multifunctional_module import create_folder_safely


def check_for_system_files(path):
	system_files_extentions = [".DS_Store"]
	return any(extention in path for extention in system_files_extentions)


def define_publication_interval(interval_hours=None):
	if interval_hours is not None:
		return int(interval_hours * 3600)
	else:
		return 4 * 3600


def get_next_image_path(directories, published_images_paths):
	for directory in directories:
		for name in os.listdir(directory):
			path = os.path.join(directory, name)
			system_file_found = check_for_system_files(path)
			if os.path.isfile(path) and not system_file_found:
				if path not in published_images_paths:
					return path
	return random.choice(published_images_paths)


def publish_content(token, chat_id, path, message='Поехали!'):
	with open(Path(f"{path}"), "rb") as file:
		document = file.read()
	time_sleep = 0
	while True:
		try:
			bot = telegram.Bot(token=token)
			bot.send_message(chat_id=chat_id, text=message)
			bot.send_document(document=document, chat_id=chat_id)
			return path
		except telegram.error.NetworkError:
			time.sleep(time_sleep)
			time_sleep += 1


def main():
	load_dotenv()
	token = os.environ['TELEGRAM_TOKEN']
	chat_id = os.environ['TELEGRAM_CHAT_ID']
	try:
		duration_sec = define_publication_interval(os.environ['PRIORITY_IMAGE_PATH'])
	except KeyError:
		duration_sec = define_publication_interval()
	main_images_folder = create_folder_safely()
	published_images_paths = []
	while True:
		directories = scout_directories(main_images_folder)
		try:
			next_image_path = os.environ['PRIORITY_IMAGE_PATH']
		except KeyError:
			next_image_path = get_next_image_path(directories, published_images_paths)
		published_image_path = publish_content(token, chat_id, next_image_path)
		published_images_paths.append(published_image_path)
		time.sleep(duration_sec)


if __name__ == "__main__":
	main()
