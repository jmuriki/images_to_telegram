import os
import time
import random

from dotenv import load_dotenv
from multifunctional_module import create_folder_safely
from multifunctional_module import get_files_paths
from multifunctional_module import find_system_files
from multifunctional_module import publish_content


def main():
    load_dotenv()
    token = os.environ["TELEGRAM_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    interval = os.getenv("PUBLICATION_INTERVAL", default=4)
    duration_sec = float(interval) * 3600
    folder = create_folder_safely()
    paths = [p for p in get_files_paths(folder) if not find_system_files(p)]
    while paths:
        for path in paths:
            publish_content(token, chat_id, path)
            time.sleep(duration_sec)
        random.shuffle(paths)


if __name__ == "__main__":
    main()
