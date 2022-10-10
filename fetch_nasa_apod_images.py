import os
import requests
import json
import time
import datetime

from dotenv import load_dotenv

from multifunctional_module import create_folder_safely
from multifunctional_module import get_extention_from_url
from multifunctional_module import compose_filename
from multifunctional_module import save_content


def get_response(url, *args):
	params = {}
	if args:
		for arg in args:
			params[arg[0]] = arg[1]
	response = requests.get(url, params=params)
	response.raise_for_status()
	return response


def fetch_nasa_apod_images(api_param, main_images_folder):
	nasa_apod_folder = create_folder_safely(main_images_folder, "nasa_apod")
	api_url = "https://api.nasa.gov/planetary/apod"
	start_date = datetime.date.today() - datetime.timedelta(days=0)
	time_sleep = 0
	while True:
		start_date_formatted = start_date.strftime("%Y-%m-%d")
		start_date_param = ["start_date", start_date_formatted]
		try:
			api_response = get_response(api_url, api_param, start_date_param).json()
		except requests.exceptions.HTTPError:
			start_date = start_date - datetime.timedelta(days=1)
			time.sleep(time_sleep)
			time_sleep += 1
		for apod_index, apod in enumerate(api_response):
			apod_url = apod.get("hdurl")
			if apod_url:
				extention = get_extention_from_url(apod_url)
				filename = compose_filename(nasa_apod_folder, apod["date"], apod_index, extention)
				content = get_response(apod_url).content
				save_content(main_images_folder, filename, content, nasa_apod_folder)
		break


def main():
	load_dotenv()
	api_key = os.environ["NASA_API_KEY"]
	api_param = ["api_key", api_key]
	main_images_folder = create_folder_safely()
	fetch_nasa_apod_images(api_param, main_images_folder)


if __name__ == "__main__":
	main()
