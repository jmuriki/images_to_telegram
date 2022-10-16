import os
import time
import requests
import telegram

from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote


def create_folder_safely(directory=".", folder_name="images"):
	Path(f"{directory}/{folder_name}").mkdir(parents=True, exist_ok=True)
	return folder_name


def compose_filepath(url, main_folder, date, secondary_folder="", index=""):
	url_part = urlparse(url).path
	unquoted_url_part = unquote(url_part)
	filename = os.path.split(unquoted_url_part)[-1]
	extention = os.path.splitext(filename)[-1]
	if index:
		index = f"_{index}"
	filename = f"{secondary_folder}_{date}{index}{extention}"
	return f"./{main_folder}/{secondary_folder}/{filename}"


def find_system_files(path):
	system_files_extentions = [".DS_Store"]
	return any(extention in path for extention in system_files_extentions)


def get_paths(folder):
	paths = []
	directories = []
	for direction in os.walk(Path(f"./{folder}")):
		directories.append(direction[0])
	for directory in directories:
		for name in os.listdir(directory):
			path = os.path.join(directory, name)
			if os.path.isfile(path) and not find_system_files(path):
				paths.append(path)
	return paths


def save_content(url, path, params=None):
	response = requests.get(url, params)
	response.raise_for_status()
	with open(Path(f"{path}"), "wb") as file:
		file.write(response.content)


def publish_content(token, chat_id, path, message="Поехали!"):
	try:
		with open(Path(f"{path}"), "rb") as file:
			document = file.read()
	except FileNotFoundError:
		print(path)
		print("Изображение не найдено.")
		return
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
