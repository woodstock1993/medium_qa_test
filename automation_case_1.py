from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os, random


url = "https://explorer.kstadium.io/"
block_height_css_selector = '#root > div.sc-jrQzAO.efokId > main > section.sc-fFeiMQ.hXmHOb > div > div:nth-child(2) > table > tbody > tr > td > a'
block_height_css_selector_2 = '#root > div > main > section > div > div > div.sc-Galmp.dlSKE > table > tbody > tr > td'
chromedriver_path = os.getcwd() + '/chromedriver'

driver = webdriver.Chrome(service=Service(f'{chromedriver_path}'), options=webdriver.ChromeOptions())


def automation_test_2(cur_url):
    """
    :param: url(string)
    :func: block height 번호를 랜덤으로 추출하여 해당 페이지로 들어간 후 번호를 대조한 후 관련 데이터를 추출하여 파일화한다.
    :return: block_height 관련 데이터 반환
    """
    global driver
    global block_height_css_selector
    global block_height_css_selector_2

    block_height_arr = []
    block_height_dic = {}

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

    try:
        block_height_number = random.choice(block_height_arr)
        print(f'block height 번호: {block_height_number}가 추출되었습니다.')
    except ValueError:
        print(f'추출된 block height 번호가 없거나 block_height_css_selector 가 잘못 설정되었습니다.')
        driver.quit()
        return

    driver.find_element(By.LINK_TEXT, str(block_height_number)).click()
    print(f'block_height_number: {block_height_number}가 클릭됨')
    sleep(2)

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    block_height_info_tags = soup.select(block_height_css_selector_2)

    data = {}

    for i in range(len(block_height_info_tags)):
        try:
            if block_height_info_tags[i].text == 'Block Height':
                data['Block Height'] = block_height_info_tags[i+1].text
            elif block_height_info_tags[i].text == 'Timestamp':
                data['Timestamp'] = block_height_info_tags[i + 1].text
            elif block_height_info_tags[i].text == 'Transactions':
                data['Transactions'] = block_height_info_tags[i + 1].text
            elif block_height_info_tags[i].text == 'Block Reward':
                data['Block Reward'] = block_height_info_tags[i + 1].text
        except IndexError:
            print(f'다음 태그가 존재하지 않습니다. {block_height_number}관련 정보가 누락됐습니다.')
            return

    try:
        cmp_block_height_number = int(data['Block Height'])
    except ValueError:
        print(f'Block Height: {data["Block Height"]} 값이 숫자가 아닙니다.')
        return

    if block_height_number == cmp_block_height_number:
        print(f'{block_height_number}가 페이지 속 {cmp_block_height_number}번호와 일치합니다.')

    driver.quit()

    return data



