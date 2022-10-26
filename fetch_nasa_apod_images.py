import os
import requests
import time
import datetime

from dotenv import load_dotenv
from multifunctional_module import create_folder_safely
from multifunctional_module import compose_filepath
from multifunctional_module import save_content


def get_apod_response(api_key, start_date):
	url = "https://api.nasa.gov/planetary/apod"
	start_date_formatted = start_date.strftime("%Y-%m-%d")
	params = {
		"api_key": api_key,
		"start_date": start_date_formatted
	}
	response = requests.get(url, params)
	response.raise_for_status()
	return response


def get_archive(api_key):
	for day in range(365):
		start_date = datetime.date.today() - datetime.timedelta(days=day)
		try:
			archive = get_apod_response(api_key, start_date).json()
			return archive
		except requests.exceptions.HTTPError:
			time.sleep(1)


def fetch_images(archive, main_folder):
	secondary_folder = create_folder_safely(main_folder, "nasa_apod")
	for apod in archive:
		apod_url = apod.get("hdurl")
		if apod_url:
			filepath = compose_filepath(
				apod_url,
				main_folder,
				apod["date"],
				secondary_folder
			)
			save_content(apod_url, filepath)


def main():
	load_dotenv()
	api_key = os.environ["NASA_API_KEY"]
	archive = get_archive(api_key)
	main_folder = create_folder_safely()
	fetch_images(archive, main_folder)


if __name__ == "__main__":
	main()
