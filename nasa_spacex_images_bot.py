import os
import time
import telegram
import random
import fetch_spacex_images
import fetch_nasa_apod_images
import fetch_nasa_epic_images

from dotenv import load_dotenv


def publish_content(image_path, text='Поехали!'):
	token = os.environ['TELEGRAM_TOKEN']
	chat_id = os.environ['CHAT_ID']
	publication_interval = os.environ['PUBLICATION_INTERVAL']
	bot = telegram.Bot(token=token)
	if not publication_interval:
		publication_interval = 3600 * 4
	else:
		publication_interval = int(3600 * publication_interval)
	bot.send_message(text=text, chat_id=chat_id)
	bot.send_document(document=open(image_path, 'rb'), chat_id=chat_id)
	time.sleep(publication_interval)



def main():
	load_dotenv()
	priority_image_path = os.environ['IMAGE_PATH']
	published_content = []
	while True:
		fetch_spacex_images.main()
		fetch_nasa_apod_images.main()
		fetch_nasa_epic_images.main()
		directories = ['./images', './images/space_x', './images/nasa_apod', './images/nasa_epic']
		for directory in directories:
			for image_name in os.listdir(directory):
				image_path = os.path.join(directory, image_name)
				if os.path.isfile(image_path):
					if priority_image_path:
						published_content.append(priority_image_path)
						publish_content(priority_image_path)
					elif image_path in published_content:
						image_path = random.choice(published_content)
						publish_content(image_path)
					else:
						published_content.append(image_path)
						publish_content(image_path)


if __name__ == "__main__":
	main()
