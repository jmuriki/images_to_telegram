import requests
import json
import argparse

from multifunctional_module import create_parser
from multifunctional_module import create_folder_safely
from multifunctional_module import get_response
from multifunctional_module import get_extention_from_url
from multifunctional_module import compose_filename
from multifunctional_module import download_content
from multifunctional_module import save_content


def get_spasex_images_links(api_response, last_launch, flight_id=""):
	if flight_id:
		links = api_response["links"]["flickr"]["original"]
	else:
		links = api_response[last_launch]["links"]["flickr"]["original"]
	return links


def get_spasex_images_date(api_response, last_launch, flight_id=""):
	if flight_id:
		date = api_response["date_local"][:10]
	else:
		date = api_response[last_launch]["date_local"][:10]
	return date


def fetch_spacex_images(main_images_folder, flight_id=""):
	space_x_folder = create_folder_safely(main_images_folder, "space_x")
	api_url = f"https://api.spacexdata.com/v5/launches/{flight_id}"
	api_response = get_response(api_url).json()
	last_launch = -1
	while True:
		links = get_spasex_images_links(api_response, last_launch, flight_id)
		date = get_spasex_images_date(api_response, last_launch, flight_id)
		if not links and flight_id:
			break
		elif not links:
			last_launch -= 1
		else:
			for link_number, link in enumerate(links):
				extention = get_extention_from_url(link)
				filename = compose_filename(space_x_folder, date, link_number, extention)
				content = download_content(link)
				save_content(main_images_folder, filename, content, space_x_folder)
			break


def main():
	main_images_folder = create_folder_safely()
	flight_id = create_parser("--id").parse_args().id
	if flight_id:
		fetch_spacex_images(main_images_folder, flight_id)
	else:
		fetch_spacex_images(main_images_folder)


if __name__ == "__main__":
	main()
