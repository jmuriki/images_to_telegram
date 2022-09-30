import requests
import json
import argparse

from pathlib import Path

from get_extention_from_url import get_extention


def fetch_spacex_images(folder, flight_id=""):
	space_x_folder_name = "space_x"
	api_url = f"https://api.spacexdata.com/v5/launches/{flight_id}"
	api_response = requests.get(api_url)
	api_response.raise_for_status()
	last_launch = -1
	while True:
		if flight_id:
			links = api_response.json()['links']['flickr']['original']
			date = api_response.json()['date_local'][:10]
		else:
			links = api_response.json()[last_launch]['links']['flickr']['original']
			date = api_response.json()[last_launch]['date_local'][:10]
		if links:
			Path(f"./{folder}/{space_x_folder_name}/").mkdir(parents=True, exist_ok=True)
			for link_number, link in enumerate(links):
				response = requests.get(link)
				response.raise_for_status()
				extention = get_extention(link)
				filename = f'space_x_{date}_{link_number}{extention}'
				with open(f"./{folder}/{space_x_folder_name}/{filename}", "wb") as file:
					file.write(response.content)
			break
		else:
			if flight_id:
				break
			else:
				last_launch -= 1
			

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument ('--id')
    return parser


def main():
	images_folder_name = 'images'
	Path(f"./{images_folder_name}").mkdir(parents=True, exist_ok=True)
	flight_id = create_parser().parse_args().id
	fetch_spacex_images(images_folder_name, flight_id)


if __name__ == "__main__":
	main()
