import os
import requests
import json
import datetime

from dotenv import load_dotenv

from multifunctional_module import create_folder_safely
from multifunctional_module import get_response
from multifunctional_module import get_extention_from_url
from multifunctional_module import compose_filename
from multifunctional_module import download_content
from multifunctional_module import save_content


def fetch_nasa_apod_images(api_key, main_images_folder):
	nasa_apod_folder = create_folder_safely(main_images_folder, "nasa_apod")
	api_url = "https://api.nasa.gov/planetary/apod"
	start_date = datetime.date.today()
	api_param = ["api_key", api_key]
	while True:
		try:
			start_date_formatted = start_date.strftime("%Y-%m-%d")
			start_date_param = ["start_date", start_date_formatted]
			api_response = get_response(api_url, api_param, start_date_param).json()
			image_id = 0
			for apod in api_response:
				apod_url = apod.get("hdurl")
				if apod_url:
					extention = get_extention_from_url(apod_url)
					filename = compose_filename(nasa_apod_folder, apod["date"], image_id, extention)
					content = download_content(apod_url)
					save_content(main_images_folder, filename, content, nasa_apod_folder)
					image_id += 1
				else:
					continue
			break
		except requests.exceptions.HTTPError:
			start_date = start_date - datetime.timedelta(days=1)


def main():
	load_dotenv()
	api_key = os.environ["NASA_API_KEY"]
	main_images_folder = create_folder_safely()
	fetch_nasa_apod_images(api_key, main_images_folder)


if __name__ == "__main__":
	main()
