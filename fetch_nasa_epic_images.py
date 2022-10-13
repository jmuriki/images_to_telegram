import os
import requests
import json

from dotenv import load_dotenv

from multifunctional_module import create_folder_safely
from multifunctional_module import compose_filepath
from multifunctional_module import save_content


def get_dates(api_param):
	url = "https://api.nasa.gov/EPIC/api/natural/all"
	response = requests.get(url, api_param)
	response.raise_for_status()
	actual_dates = response.json()
	date = actual_dates[0]["date"]
	date_formatted = date.replace("-","/")
	return date, date_formatted


def get_archive(date, api_param):
	url = f"https://api.nasa.gov/EPIC/api/natural/date/{date}"
	response = requests.get(url, api_param)
	response.raise_for_status()
	archive = response.json()
	return archive


def get_epic_url(date_formatted, image_name):
	url = "https://api.nasa.gov/EPIC/archive/natural/"
	epic_url = f"{url}{date_formatted}/png/{image_name}.png"
	return epic_url


def fetch_images(api_param, main_folder):
	secondary_folder = create_folder_safely(main_folder, "nasa_epic")
	date, date_formatted = get_dates(api_param)
	archive = get_archive(date, api_param)
	for index, epic in enumerate(archive):
		epic_url = get_epic_url(date_formatted, epic['image'])
		filepath = compose_filepath(
			epic_url,
			main_folder,
			date,
			secondary_folder,
			index
		)
		save_content(epic_url, filepath, api_param)


def main():
	load_dotenv()
	api_key = os.environ["NASA_API_KEY"]
	api_param = {"api_key": api_key}
	main_folder = create_folder_safely()
	fetch_images(api_param, main_folder)


if __name__ == "__main__":
	main()
