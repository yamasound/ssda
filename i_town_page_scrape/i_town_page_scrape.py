#!/usr/bin/env python3

USAGE = '''
[USAGE]
./command.sh area keyword

[SAMPLE]
./command.sh 豊橋市 コンビニエンスストア
'''

import csv, glob, sys
from pathlib import Path
from bs4 import BeautifulSoup

from crawler import Crawler
    
class ITwonPage():
    def load_html(self, path):
        print('loading', path)
        with open(path, 'r', encoding='utf-8') as f:
            html = str(f.readlines())
        return html

    def _iter_name_address(self, path):
        def get_text(div, cls):
            return div.find(class_=cls).get_text(strip=True).split('\\n')[0]
        html = self.load_html(path)
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
    
    def extract_data(self, area, keyword):
        with open(f"output/{area}_{keyword}/address.csv", 'w') as f:
            writer = csv.writer(f)
            input_regexp = f"output/{area}_{keyword}/leaf/*.html"
            for path_name in sorted(glob.glob(input_regexp)):
                for name, address in self._iter_name_address(Path(path_name)):
                    row = [name, address]
                    print(row)
                    writer.writerow(row)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        area, keyword = sys.argv[1:3]
        Crawler().crawl(area, keyword)
        ITwonPage().extract_data(area, keyword)
    else:
        print(USAGE)
