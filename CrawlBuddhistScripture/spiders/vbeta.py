import scrapy
import json
from bs4 import BeautifulSoup

class VbetaSpider(scrapy.Spider):
    name = "vbeta"
    start_urls = [
        'https://api.phapbao.org/api/categories/get-selectlist-categories?hasAllOption=false',
        'https://api.phapbao.org/api/search/get-books-by-categoryId',
        'https://api.phapbao.org/api/search/get-tableofcontents-by-bookId',
        'https://api.phapbao.org/api/search/get-pages-by-tableofcontentid/'
    ]
    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            method="GET",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            callback=self.parse,
        )
    
    def parse(self, response):
        data_stype = json.loads(response.body)
        for item in data_stype['result']:
            json_data = json.dumps({"id": item['value']})
            yield scrapy.Request(
                url=self.start_urls[1],
                method="POST",
                body=json_data,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                callback=self.parse_style,
            )
    
    def parse_style(self, response):
        data = json.loads(response.body)
        
        for item in data['result']['items']:
            json_data = json.dumps({"id": item['id']})
            yield scrapy.Request(
                            url=self.start_urls[2],
                            method="POST",
                            body=json_data,
                            headers={"Content-Type": "application/json", "Accept": "application/json"},
                            callback=self.parse_book,
                            meta={"item_book": item}
                        )
    
    def parse_book(self, response):
        data_menu = json.loads(response.body)
        for item in data_menu['result']['tableOfContents']['items']:
            yield scrapy.Request(
                            url=self.start_urls[3] + str(item['id']),
                            method="GET",
                            headers={"Content-Type": "application/json", "Accept": "application/json"},
                            callback=self.parse_menu,
                            meta={"item_book": response.meta["item_book"], "item_menu": item}
                        )
    
    def parse_menu(self, response):
        data_text = json.loads(response.body)
        item_book = response.meta["item_book"]
        item_menu = response.meta["item_menu"]
        dictnew = {
            "name": item_book['name'],
            "author": item_book['author'],
            "categoryName": item_book['categoryName'],
            "publicationYear": item_book['publicationYear'],
            "chapter": item_menu['name'],
            'content': [span.get_text(strip=True) for html in data_text['result']['pages'] for span in BeautifulSoup(html['htmlContent'], 'html.parser').find_all('span')]
        }
        yield dictnew
        