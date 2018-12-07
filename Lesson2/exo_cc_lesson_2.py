import requests 
from bs4 import BeautifulSoup


website_base = 'https://www.darty.com/nav/achat/informatique/ordinateur_portable/portable/'
def _handle_request_and_get_soup(request_result):
	if request_result.status_code == 200:
		html_doc =  request_result.text
		soup = BeautifulSoup(html_doc,"html.parser")
	return soup

def get_all_laptops_prices(soup):
	return soup.find_all(class_='darty_prix_barre_remise')

def main():
	
	sp = _handle_request_and_get_soup(requests.get(website_base + "marque__dell__DELL.html"))
	res = get_all_laptops_prices(sp)
	print res
if __name__ == '__main__':
	main()
	
