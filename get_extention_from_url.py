import os

from urllib.parse import urlparse
from urllib.parse import unquote


def get_extention(url):
	url_part = urlparse(url).path
	unquoted_url_part = unquote(url_part)
	filename = os.path.split(unquoted_url_part)[-1]
	extention = os.path.splitext(filename)[-1]
	return extention


if __name__ == "__main__":
	get_extention(url)
