from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
import os


url = "https://explorer.kstadium.io/"
block_height_css_selector = '#root > div.sc-jrQzAO.efokId > main > section.sc-fFeiMQ.hXmHOb > div > div:nth-child(2) > table > tbody > tr > td > a'
click_x_path = ''
chromedriver_path = os.getcwd() + '/chromedriver'

driver = webdriver.Chrome(service=Service(f'{chromedriver_path}'), options=webdriver.ChromeOptions())


def check_block_height(cur_url):
    global driver
    global block_height_css_selector

    block_height_arr = []

    driver.get(cur_url)
    sleep(2)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    block_height_tags = soup.select(f'{block_height_css_selector}')

    for block in block_height_tags:
        a_info = block['href']
        if a_info.endswith("txs"):
            li = block['href'].split('/')
            block_height = li[2]
            try:
                block_height_arr.append(int(block_height))
            except ValueError:
                print(f'block_height: {block_height} 가 숫자 형태가 아닙니다')

    driver.quit()

    return block_height_arr


print(check_block_height(url))
