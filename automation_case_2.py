from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
import os

url = "https://explorer.kstadium.io/"
image_extension = '.png'
one_exist = False
number_exist = False


def create_folder(added_path):
    """
    :param added_path: 현재 경로에 폴더(/폴더이름)을 포함한 경로를 추가로 적어준다.
    :function: 덧붙인 경로에 폴더를 생성한다. 같은 이름이 있으면 폴더를 생성하지 않는다.
    :return: 해당 폴더가 위치한 경로를 반환한다.
    """
    current_path = os.getcwd()
    path = current_path + added_path
    if not os.path.exists(path):
        os.mkdir(path)
        print(f'{path}경로에 폴더가 생성되었습니다')
    return path


def return_latest_jpg_number(path_dir):
    """
    :param path_dir: 현재 경로에 덧붙일 폴더(/폴더이름)을 포함한 경로를 적어준다.
    :return: 폴더 내에 숫자만으로 이루어진 이름이 있을 경우 그 중에서 가장 큰 번호를 반환한다. 없을 경우 1을 반환한다.
    """
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
            if file_list[i].endswith(image_extension):
                li = file_list[i].split(image_extension)
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


"""
    - 현재 경로에 /automation_case_2 폴더 생성
    - 드라이버 설정
    - automation_case_2 폴더 내 파일 번호 반환
    - global 변수
        - cur_page: 접속한 url 페이지를 나타내는 번호
        - enter: 사용자 함수가 한번 실행 됐음을 체크하는 bool
        - enter_2: 사용자 함수 내 재귀함수가 실행 됐음을 체크하는 bool
        - transaction_check: 1이 나왔음을 체크하는 bool
        - block_height_css_selector: 접속한 페이지 내 tag를 불러오기 위한 선택자
        - click_x_path: 트랜잭션 값이 1이 나오지 않았을 때 다음 페이지로 넘어가기 위해 필요한 선택자  
"""

folder_path = create_folder('/automation_case_2')
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
    """
    :param cur_url: 접속할 페이지 url
    :function: block num 의 transaction 이 1이 나타날 때까지 다음 페이지로 이동하면서 방문한 페이지의 화면을 스크린샷으로 찍어 지정한 폴더 경로에 저장한다.
    :return: None
    """
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
    block_height_tags = soup.select(block_height_css_selector)

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
                print(f'block_height or transaction 이 숫자형태가 아닙니다')
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
        driver.find_element('xpath', click_x_path).click()
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
    """
    :function: transaction 1을 찾기 위해 search_block_height 함수가 돈 횟수를 출력한다.
    :return: None
    """
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
