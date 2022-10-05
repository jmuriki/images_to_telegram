import os
import requests
import argparse

from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote


def check_for_system_files(path):
	system_files_extentions = [".DS_Store"]
	return any(extention in path for extention in system_files_extentions)


def scout_directories(folder_name=""):
	directories = []
	for direction in os.walk(Path(f'{folder_name}')):
		directories.append(direction[0])
	return directories


def create_parser(argument_name):
    parser = argparse.ArgumentParser()
    parser.add_argument(argument_name)
    return parser


def create_folder_safely(directory=".", folder_name="images"):
	Path(f"{directory}/{folder_name}").mkdir(parents=True, exist_ok=True)
	return folder_name


def get_response(url, *args):
	params = {}
	if args:
		for arg in args:
			params[arg[0]] = arg[1]
	response = requests.get(url, params=params)
	response.raise_for_status()
	return response


def get_extention_from_url(url):
	url_part = urlparse(url).path
	unquoted_url_part = unquote(url_part)
	filename = os.path.split(unquoted_url_part)[-1]
	extention = os.path.splitext(filename)[-1]
	return extention


def compose_filename(folder_name, date, index, extention):
	return f"{folder_name}_{date}_{index + 1}{extention}"


def download_content(url, api_param=""):
	if api_param:
		return get_response(url, api_param).content
	else:
		return get_response(url).content


def save_content(main_folder, filename, content, secondary_folder=""):
	with open(Path(f"./{main_folder}/{secondary_folder}/{filename}"), "wb") as file:
		file.write(content)


def main():
	pass


if __name__ == "__main__":
	main()
