from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import os

url = "https://explorer.kstadium.io/"
image_extension = '.png'
one_exist = False
number_exist = False


# 드라이버 설정
def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver


# 인자로 현재 경로에 덧붙일 경로를 넣는다. 폴더 경로를 덧붙여 설정해주어야 한다.
def create_folder(added_path):
    current_path = os.getcwd()
    path = current_path + added_path
    if not os.path.exists(path):
        os.mkdir(path)
        print(f'{path}경로에 폴더가 생성되었습니다')
    return path


# 최신파일 번호를 리턴한다. 번호로 된 파일이 없으면 새 시작을 의미하는 1을 리턴한다.
def return_latest_jpg_number(path_dir):
    global one_exist
    global number_exist
    num_arr = []
    global image_extension
    file_list = os.listdir(path_dir)
    file_num = len(file_list)
    if file_num == 0:
        return 1
    else:
        for i in range(file_num):
            if file_list[i].endswith(f'{image_extension}'):
                li = file_list[i].split(f'{image_extension}')
                try:
                    file_name = int(li[0])
                    num_arr.append(file_name)
                except ValueError:
                    continue
        try:
            if num_arr[-1]:
                if 1 in num_arr:
                    one_exist = True
                    number_exist = True
                return max(num_arr)
        except TypeError:
            pass
    return 1


folder_path = create_folder('/case_2_screen_shot')
chromedriver_path = os.getcwd() + '/chromedriver'
driver = webdriver.Chrome(service=Service(f'{chromedriver_path}'), options=webdriver.ChromeOptions())
png_num = return_latest_jpg_number(folder_path)
print(f'현재 {folder_path} 경로 내 가장 큰 png 번호: {png_num}')

cur_page = 1
enter = False
enter_2 = False
transaction_check = False
block_height_css_selector = '#root > div.sc-jrQzAO.efokId > main > section.sc-fFeiMQ.hXmHOb > div > div:nth-child(2) > table > tbody > tr > td > a'
click_x_path = '//*[@id="root"]/div[2]/main/section[2]/div/div[2]/div/span[2]/a'


def search_block_height(cur_url):
    global driver
    global folder_path
    global png_num
    global cur_page
    global enter
    global enter_2
    global transaction_check
    global block_height_css_selector
    global click_x_path

    screen_image_name = f'{folder_path}/{png_num}{image_extension}'

    if enter is False:
        driver.get(cur_url)
        enter = True
    sleep(2)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    block_height_tags = soup.select(f'{block_height_css_selector}')

    temp_dic = {}
    for block in block_height_tags:
        a_info = block['href']
        if a_info.endswith("txs"):
            li = block['href'].split('/')
            block_height = li[2]
            transaction = block.text
            try:
                block_height = int(block_height)
                transaction = int(transaction)
                temp_dic[block_height] = transaction
                if transaction == 1:
                    transaction_check = True
            except ValueError:
                print(f'block_height or transaction이 숫자형태가 아닙니다')
                continue
    if transaction_check is True and one_exist is False and png_num == 1:
        driver.save_screenshot(screen_image_name)
        driver.quit()
        return
    elif transaction_check is True and png_num == 1 and one_exist is True:
        png_num += 1
        screen_image_name = f'{folder_path}/{png_num}{image_extension}'
        driver.save_screenshot(screen_image_name)
        driver.quit()
        return
    elif transaction_check is True and png_num != 1 and number_exist is True and enter_2 is False:
        png_num += 1
        screen_image_name = f'{folder_path}/{png_num}{image_extension}'
        driver.save_screenshot(screen_image_name)
        driver.quit()
        return
    elif transaction_check is False:
        if number_exist is True and enter_2 is False:
            png_num += 1
            screen_image_name = f'{folder_path}/{png_num}{image_extension}'
        enter_2 = True
        driver.save_screenshot(screen_image_name)
        png_num += 1
        driver.find_element('xpath', f'{click_x_path}').click()
        cur_page += 1
        print(f'transaction 1을 찾기 위해 {cur_page}번 페이지로 이동하였습니다.')
        sleep(2)
        cur_url = driver.current_url
        search_block_height(cur_url)
        return
    screen_image_name = f'{folder_path}/{png_num}{image_extension}'
    driver.save_screenshot(screen_image_name)
    driver.quit()
    return


def print_result():
    global cur_page
    global enter
    global enter_2

    if png_num == 1:
        print('1번만 돔')
    elif enter is True and enter_2 is False:
        print('1번만 돔')
    elif enter is True and enter_2 is True:
        print(f'최종적으로 {cur_page}번 페이지까지 이동하였습니다.')


search_block_height(url)
print_result()
