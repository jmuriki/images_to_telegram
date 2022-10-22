import os
import time
import requests
import telegram
import argparse

from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote


def create_parser(argument_name):
    parser = argparse.ArgumentParser()
    parser.add_argument(argument_name, default="")
    return parser


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


def get_files_paths(folder):
	paths = []
	for root, _, files in os.walk(Path(f"./{folder}")):
		for name in files:
			path = os.path.join(root, name)
			paths.append(path)
	return paths


def save_content(url, path, params=None):
	response = requests.get(url, params)
	response.raise_for_status()
	with open(Path(f"{path}"), "wb") as file:
		file.write(response.content)


def publish_content(token, chat_id, path):
	try:
		with open(Path(path), "rb") as file:
			document = file.read()
	except IsADirectoryError:
		raise
	bot = telegram.Bot(token=token)
	time_sleep = 0
	while True:
		try:
			bot.send_document(document=document, chat_id=chat_id, caption="Поехали!")
			return True
		except telegram.error.NetworkError:
			time.sleep(time_sleep)
			time_sleep += 1
