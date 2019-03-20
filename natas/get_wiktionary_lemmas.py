import requests
from bs4 import BeautifulSoup
from mikatools import *


url = "https://en.wiktionary.org/w/index.php?title=Category:English_lemmas&from=A"
base_url = "https://en.wiktionary.org/"

def get_pages(url):
	all_lemmas = []
	while True:
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		base = soup.find("div", id="mw-pages")
		lemmas = base.find_all("li")
		for lemma in lemmas:
			text = lemma.get_text()
			all_lemmas.append(text)
		next_button = base.find("a", string="next page")
		if next_button is None:
			break
		url = base_url + next_button.get("href")
	return all_lemmas

