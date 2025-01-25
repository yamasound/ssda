#!/usr/bin/env python3

from bs4 import BeautifulSoup

class Parser():
    def _load_html(self, path):
        print('loading', path)
        with open(path, 'r', encoding='utf-8') as f:
            html = str(f.readlines())
        return html
    
    def _iter_name_address(self, path):
        def get_text(div, cls):
            return div.find(class_=cls).get_text(strip=True).split('\\n')[0]
        html = self._load_html(path)
        soup = BeautifulSoup(html, 'html.parser')
        divs = soup.select('.result-list>div')
        l_name_address = []
        for i, div in enumerate(divs, 1):
            try:
                name = get_text(div, 'result-item-head__ttl')
                address = get_text(div, 'result-item-cts-desc__area')
                yield name, address
            except:
                pass
