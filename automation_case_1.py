from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
import os, random


url = "https://explorer.kstadium.io/"
block_height_css_selector = '#root > div.sc-jrQzAO.efokId > main > section.sc-fFeiMQ.hXmHOb > div > div:nth-child(2) > table > tbody > tr > td > a'
click_x_path = ''
chromedriver_path = os.getcwd() + '/chromedriver'

driver = webdriver.Chrome(service=Service(f'{chromedriver_path}'), options=webdriver.ChromeOptions())


def check_block_height(cur_url):
    """
    :param: url(string)
    :return: block_height 의 번호가 담긴 리스트 중 추출하여 block_height 반환
    """
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

    try:
        block_height_number = random.choice(block_height_arr)
        print(f'block height 번호: {block_height_number}가 추출되었습니다.')
        return block_height_number
    except ValueError:
        print(f'추출된 block height 번호가 없거나 block_height_css_selector 가 잘못 설정되었습니다.')

    print(f'url, webdriver, css_선택자를 재고하여 오류를 찾아내십시오')
    return


