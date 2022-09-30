import os
import requests
import json
import datetime

from pathlib import Path
from dotenv import load_dotenv

from get_extention_from_url import get_extention


def fetch_nasa_apod_images(folder):
	api_key = os.environ['NASA_API_KEY']
	nasa_folder_name = "nasa_apod"
	api_url = "https://api.nasa.gov/planetary/apod"
	start_date = datetime.date.today()
	while True:
		try:
			date_formatted = start_date.strftime("%Y-%m-%d")
			params = {
				"api_key": api_key,
				"start_date": date_formatted,
			}
			api_response = requests.get(api_url, params=params)
			api_response.raise_for_status()
			Path(f"./{folder}/{nasa_folder_name}/").mkdir(parents=True, exist_ok=True)
			for apod in api_response.json():
				apod_url = apod.get('hdurl')
				if apod_url:
					response = requests.get(apod_url)
					response.raise_for_status()
					extention = get_extention(apod_url)
					filename = f"nasa_apod_{apod['date']}{extention}"
					with open(f"./{folder}/{nasa_folder_name}/{filename}", "wb") as file:
						file.write(response.content)
				else:
					continue
			break
		except requests.exceptions.HTTPError:
			start_date = start_date - datetime.timedelta(days=1)


def main():
	load_dotenv()
	images_folder_name = 'images'
	Path(f"./{images_folder_name}").mkdir(parents=True, exist_ok=True)
	fetch_nasa_apod_images(images_folder_name)


if __name__ == "__main__":
	main()
