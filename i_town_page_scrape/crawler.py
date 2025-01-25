#!/usr/bin/env python3

import copy, os, pyautogui, random, time, urllib
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

from parser import Parser

class Crawler(Parser):
    def __init__(self, max_leafs=False):
        self.url = 'https://itp.ne.jp'
        self.dir_poi = 'output/poi'
        self.max_leafs = max_leafs
        
    def _create_driver(self, url):
        opt = webdriver.ChromeOptions()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        opt.add_argument(f"--user-agent={user_agent}")
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=opt)
        driver.set_window_position(0, 0)
        driver.set_window_size(640, 800)
        driver.implicitly_wait(10)
        driver.get(url)
        return driver
    
    def _sleep(self):
        time.sleep(random.randint(1,5))
        
    def _search(self, driver, area, keyword):
        driver.find_element(By.ID, 'form1').find_element(
            By.ID, 'keyword').send_keys(area)
        driver.find_element(By.ID, 'form1').find_element(
            By.NAME, 'word').send_keys(keyword)
        driver.find_element(By.ID, 'form1').find_element(
            By.TAG_NAME, 'button').click()
        try:
            self._sleep()
            pyautogui.click(252, 444)
            self._sleep()
            pyautogui.click(315, 515)
        except:
            pass
        quote_elements = WebDriverWait(driver, 240).until(
            EC.presence_of_all_elements_located((
                By.ID, 'footer')))
        return driver
    
    def _update_url(self, url, pg):
        pu = urllib.parse.urlparse(url)
        d = urllib.parse.parse_qs(pu.query)
        d['PG'] = str(pg)
        return urllib.parse.urlunparse(pu._replace(
            query=urllib.parse.urlencode(d, doseq=True)))
    
    def _save_html(self, path, html):
        os.makedirs(path.parent, exist_ok=True)
        print('saving', path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
                    
    def crawl(self, area, keyword):
        def get_driver():
            driver = self._create_driver(self.url)
            driver = self._search(driver, area, keyword)
            return driver
        
        def check_html():
            rows = [[_]
                    for _, __ in self._iter_name_address(path)]
            return True if len(rows) > 0 else False

        driver = False
        f = 0; pg = 1
        while f < 4 and (
                pg <= self.max_leafs or not self.max_leafs):
            
            print(f"Getting html for pg {pg} ... ")
            if not driver:
                driver = get_driver()
            url = self._update_url(driver.current_url, pg)
            path = Path(f"output/{area}_{keyword}/leaf/{pg}.html")
            try:
                driver.get(url)
                self._save_html(path, driver.page_source)
                if not check_html():
                    raise
                print(f"success.")
                f = 0; pg += 1
            except:
                print(f"failed.")
                f += 1
                driver.quit()
                driver = False
                time.sleep(200)
            self._sleep()
        if driver:
            driver.quit()
        
if __name__ == '__main__':
    c = Crawler(max_leafs=2) # 0: 全て
    c.crawl(area='豊橋市', keyword='コンビニエンスストア')
