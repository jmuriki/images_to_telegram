import os
import requests

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


def compose_filepath(url, main_folder, date, secondary_folder="", index=""):
	url_part = urlparse(url).path
	unquoted_url_part = unquote(url_part)
	filename = os.path.split(unquoted_url_part)[-1]
	extention = os.path.splitext(filename)[-1]
	if index or index == 0:
		index = f"_{index + 1}"
	filename = f"{secondary_folder}_{date}{index}{extention}"
	return f"./{main_folder}/{secondary_folder}/{filename}"


def save_content(url, path, params=None):
	response = requests.get(url, params)
	response.raise_for_status()
	with open(Path(f"{path}"), "wb") as file:
		file.write(response.content)
