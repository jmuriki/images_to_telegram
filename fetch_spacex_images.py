import requests
import json
import argparse

from multifunctional_module import create_folder_safely
from multifunctional_module import compose_filepath
from multifunctional_module import save_content


def create_parser(argument_name):
    parser = argparse.ArgumentParser()
    parser.add_argument(argument_name, default="")
    return parser


def get_spacex_response(flight_id):
	api_url = f"https://api.spacexdata.com/v5/launches/{flight_id}"
	response = requests.get(api_url)
	response.raise_for_status()
	return response.json() if not flight_id else [response.json()]


def parse_response(spacex_response):
	for day in spacex_response[::-1]:
		date = day["date_local"][:10]
		links = day["links"]["flickr"]["original"]
		if date and links:
			return date, links


def fetch_images(main_folder, links, date):
	secondary_folder = create_folder_safely(main_folder, "space_x")
	for link_number, link in enumerate(links, start=1):
		filepath = compose_filepath(
			link,
			main_folder,
			date,
			secondary_folder,
			link_number
		)
		save_content(link, filepath)


def main():
	main_folder = create_folder_safely()
	flight_id = create_parser("--id").parse_args().id
	spacex_response = get_spacex_response(flight_id)
	date, links = parse_response(spacex_response)
	fetch_images(main_folder, links, date)


if __name__ == "__main__":
	main()
