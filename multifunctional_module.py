import os

from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote


def scout_directories(folder_name=""):
	directories = []
	for direction in os.walk(Path(f'{folder_name}')):
		directories.append(direction[0])
	return directories


def create_folder_safely(directory=".", folder_name="images"):
	Path(f"{directory}/{folder_name}").mkdir(parents=True, exist_ok=True)
	return folder_name


def get_extention_from_url(url):
	url_part = urlparse(url).path
	unquoted_url_part = unquote(url_part)
	filename = os.path.split(unquoted_url_part)[-1]
	extention = os.path.splitext(filename)[-1]
	return extention


def compose_filename(folder_name, date, index, extention):
	return f"{folder_name}_{date}_{index + 1}{extention}"


def save_content(main_folder, filename, content, secondary_folder=""):
	with open(Path(f"./{main_folder}/{secondary_folder}/{filename}"), "wb") as file:
		file.write(content)
