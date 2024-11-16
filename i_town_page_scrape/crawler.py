#!/usr/bin/env python3

import os, time
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Crawler():
    def __init__(self, max_leafs=False, max_pois_per_leaf=-1):
        self.url = 'https://itp.ne.jp'
        self.dir_poi = 'output/poi'
        self.max_leafs = max_leafs
        self.max_pois_per_leaf = max_pois_per_leaf
        
    def _create_driver(self, url, headless):
        opt = webdriver.ChromeOptions()
        if headless:
            opt.add_argument('--headless')
        opt.add_argument('--no-sandbox')
        opt.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=opt)
        if not headless:
            driver.set_window_size(640, 800)
            driver.set_window_position(0, 0)
        driver.implicitly_wait(10)
        driver.get(url)
        return driver
    
    def _save_html(self, path, html):
        os.makedirs(path.parent, exist_ok=True)
        print('saving', path)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
            
    def _search(self, driver, area, keyword):
        driver.find_element(By.ID, 'form1'
                            ).find_element(By.ID, 'keyword').send_keys(area)
        driver.find_element(By.ID, 'form1'
                            ).find_element(By.NAME, 'word').send_keys(keyword)
        driver.find_element(By.ID, 'form1'
                            ).find_element(By.TAG_NAME, 'button').click()
        quote_elements = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.ID, 'footer')))
    
    def _move_next_leaf(self, driver):
        url = driver.find_element(
            By.CLASS_NAME, 'pager').find_element(
                By.CLASS_NAME, 'next').find_element(
                    By.CLASS_NAME, 'active').get_attribute('href')
        driver.get(url)
    
    def _iter_poi_url(self, driver):
        divs = driver.find_element(By.CLASS_NAME, 'result-list'
                                   ).find_elements(By.XPATH, './div')
        for i, div in enumerate(divs):
            if div.get_attribute('class') not in ['', 'pager']:
                yield div.find_element(By.TAG_NAME, 'a').get_attribute('href')
                
    def _crawl_pois(self, driver, area, keyword, i):
        j = 0
        for poi_url in self._iter_poi_url(driver):
            j += 1
            if self.max_pois_per_leaf == -1:
                continue
            if j <= self.max_pois_per_leaf or not self.max_pois_per_leaf:
                with self._create_driver(poi_url, headless=True) as d:
                    path = Path(f"output/{area}_{keyword}/poi/{i}_{j}.html")
                    self._save_html(path, d.page_source)
                time.sleep(1)
            else:
                break
        return j
    
    def crawl(self, area, keyword):
        driver = self._create_driver(self.url, headless=False)
        self._search(driver, area, keyword)
        i = 0
        while i < self.max_leafs or not self.max_leafs:
            i += 1
            j = self._crawl_pois(driver, area, keyword, i)
            if j > 0:
                path = Path(f"output/{area}_{keyword}/leaf/{i}.html")
                self._save_html(path, driver.page_source)
            try:
                self._move_next_leaf(driver)
            except:
                break
            time.sleep(1)
        driver.quit()
        
if __name__ == '__main__':
    c = Crawler(
        max_leafs=2, # 0: 全て
        max_pois_per_leaf=-1)  # -1: 無し, 0: 全て
    c.crawl(area='豊橋市', keyword='コンビニエンスストア')
