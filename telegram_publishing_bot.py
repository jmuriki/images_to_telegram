import os
import time
import telegram
import random
import requests

from dotenv import load_dotenv
from pathlib import Path

from multifunctional_module import scout_directories
from multifunctional_module import create_folder_safely
from multifunctional_module import check_for_system_files


def define_publication_interval(interval_hours):
	if interval_hours:
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
	connection_error = 0
	while True:
		if connection_error > 1:
			time.sleep(60)
		try:
			bot = telegram.Bot(token=token)
			bot.send_message(chat_id=chat_id, text=message)
			bot.send_document(document=document, chat_id=chat_id)
			return path
		except telegram.error.NetworkError:
			connection_error += 1


def main():
	load_dotenv()
	token = os.environ['TELEGRAM_TOKEN']
	chat_id = os.environ['TELEGRAM_CHAT_ID']
	priority_image_path = os.environ['PRIORITY_IMAGE_PATH']
	interval_hours = os.environ['PUBLICATION_INTERVAL']
	main_images_folder = create_folder_safely()
	published_images_paths = []
	while True:
		directories = scout_directories(main_images_folder)
		if priority_image_path:
			next_image_path = priority_image_path
		else:
			next_image_path = get_next_image_path(directories, published_images_paths)
		published_image_path = publish_content(token, chat_id, next_image_path)
		published_images_paths.append(published_image_path)
		duration_sec = define_publication_interval(interval_hours)
		time.sleep(duration_sec)


if __name__ == "__main__":
	main()
