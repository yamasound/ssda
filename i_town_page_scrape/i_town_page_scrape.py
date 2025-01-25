#!/usr/bin/env python3

USAGE = '''
[USAGE]
./command.sh area keyword

[SAMPLE]
./command.sh 豊橋市 コンビニエンスストア
'''

import csv, glob, sys
from pathlib import Path

from crawler import Crawler
from parser import Parser
    
class ITwonPage(Parser):
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
