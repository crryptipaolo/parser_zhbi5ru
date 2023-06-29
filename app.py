from requests import get
from bs4 import BeautifulSoup as Bs
import csv
import traceback

def get_html(url , headers = None, params = None):
	try:
		html = get(url, headers = headers, params = params)
		if html.status_code == 200:
			return html.text
	except Exception as err:
		print(traceback.format_exc())
		return None

def get_price(url):
	html = get_html(url)
	if html:
		soup = Bs(html, 'lxml')
		items = soup.find('ul', class_ = 'price-block').find_all('li')
		price = items[1].text.strip()
		price = ''.join(price.split(' ')[:-1])
		return price
	else:
		return None

def parse(soup):
	root = 'http://zhbi5.ru'
	results = []
	rows = soup.find('table').find_all('tr')
	if rows:
		for index, row in enumerate(rows):
			if index < 2:
				continue
			result = {}
			columns = row.find_all('td')
			if columns:
				result['title'] = columns[1].text
				result['descr'] = f'{columns[3].text}*{columns[4].text}*{columns[5].text}'
				price = get_price(root + row.get('link'))
				if price:
					result['price'] = price
				results.append(result)
	return results

def save_to_csv(fileName, records, headers):
	try:
		with open(fileName, 'w') as f:
			writer = csv.writer(f, delimiter = ';', quotechar = '"', lineterminator = '\n')
			writer.writerow(headers)
			for record in records:
				writer.writerow(record.values())
	except IOError as err:
		raise	


def main():
	url = 'http://zhbi5.ru/catalog/dorozhnoe_stroitelstvo/zhelezobetonnye_koroba_kb_dlya_udlineniya_ustoev_zheleznodorozhnykh_mostov_po_serii_3_501_1_167_vypu/'
	html = get_html(url)
	if html:
		soup = Bs(html, 'lxml')
		results = parse(soup)
		if results:
			headers = ['Наименование', 'Размеры']
			save_to_csv('results.csv', results, headers)

if __name__ == '__main__':
	main()