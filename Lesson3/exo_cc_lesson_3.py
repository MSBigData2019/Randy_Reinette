import requests 
from bs4 import BeautifulSoup

def _handle_request_and_get_soup(request_result):
	if request_result.status_code == 200:
        	html_doc =  request_result.text
        	soup = BeautifulSoup(html_doc,"html.parser")
    	return soup

def get_top_cities(soup):
	raw_list = soup.find('tbody').findAll('a')
	city_list = []
	for city in raw_list: 
