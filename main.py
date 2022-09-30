import os
import requests
import json
import datetime

from pathlib import Path
from urllib.parse import urlparse
from urllib.parse import unquote
from dotenv import load_dotenv


def get_extention(url):
	url_part = urlparse(url).path
	unquoted_url_part = unquote(url_part)
	filename = os.path.split(unquoted_url_part)[-1]
	extention = os.path.splitext(filename)[-1]
	return extention


def fetch_spacex_last_launch(folder):
	space_x_folder_name = "space_x"
	space_x_api_url = "https://api.spacexdata.com/v5/launches/"
	space_x_api_response = requests.get(space_x_api_url)
	space_x_api_response.raise_for_status()
	last_launch = -1
	while True:
		links = space_x_api_response.json()[last_launch]['links']['flickr']['original']
		if links:
			Path(f"./{folder}/{space_x_folder_name}/").mkdir(parents=True, exist_ok=True)
			date = space_x_api_response.json()[last_launch]['date_local'][:10]
			for link_number, link in enumerate(links):
				response = requests.get(link)
				response.raise_for_status()
				extention = get_extention(link)
				filename = f'space_x_{date}_{link_number}{extention}'
				with open(f"./{folder}/{space_x_folder_name}/{filename}", "wb") as file:
					file.write(response.content)
			break
		else:
			last_launch -= 1


def fetch_nasa_apod(folder):
	api_key = os.environ['NASA_API_KEY']
	nasa_folder_name = "nasa"
	nasa_apod_api_url = "https://api.nasa.gov/planetary/apod"
	period = 3
	start_date = datetime.date.today() - datetime.timedelta(days=period)
	while True:
		try:
			date_formatted = start_date.strftime("%Y-%m-%d")
			params = {
				"api_key": api_key,
				"start_date": date_formatted,
			}
			nasa_apod_api_response = requests.get(nasa_apod_api_url, params=params)
			nasa_apod_api_response.raise_for_status()
			for apod in nasa_apod_api_response.json():
				apod_url = apod.get('hdurl')
				if apod_url:
					response = requests.get(apod_url)
					response.raise_for_status()
					extention = get_extention(apod_url)
					filename = f"nasa_apod_{apod['date']}{extention}"
					Path(f"./{folder}/{nasa_folder_name}/").mkdir(parents=True, exist_ok=True)
					with open(f"./{folder}/{nasa_folder_name}/{filename}", "wb") as file:
						file.write(response.content)
				else:
					continue
			break
		except requests.exceptions.HTTPError:
			start_date = start_date - datetime.timedelta(days=1)


def fetch_nasa_epic(folder):
	api_key = os.environ['NASA_API_KEY']
	nasa_folder_name = "nasa"
	params = {
	"api_key": api_key
	}
	archive_url = "https://api.nasa.gov/EPIC/archive/natural/"
	actual_dates_url = "https://api.nasa.gov/EPIC/api/natural/all"
	response = requests.get(actual_dates_url, params=params)
	response.raise_for_status()
	last_actual_date = response.json()[0]['date']
	formatted_date = last_actual_date.replace('-','/')
	last_actual_date_url = f"https://api.nasa.gov/EPIC/api/natural/date/{last_actual_date}"
	response = requests.get(last_actual_date_url, params=params)
	response.raise_for_status()
	nasa_archive = response.json()
	Path(f"./{folder}/{nasa_folder_name}/").mkdir(parents=True, exist_ok=True)
	image_id = 0
	for element in nasa_archive:
		epic_image_url = f"{archive_url}{formatted_date}/png/{element['image']}.png"
		response = requests.get(epic_image_url, params=params)
		response.raise_for_status()
		filename = f'nasa_epic_{last_actual_date}_{image_id}.png'
		with open(f"./{folder}/{nasa_folder_name}/{filename}", "wb") as file:
			file.write(response.content)
		image_id += 1


def main():
	load_dotenv()
	images_folder_name = 'images'
	Path(f"./{images_folder_name}").mkdir(parents=True, exist_ok=True)
	fetch_spacex_last_launch(images_folder_name)
	fetch_nasa_apod(images_folder_name)
	fetch_nasa_epic(images_folder_name)


if __name__ == "__main__":
	main()
