from utils.commons import *

url = "https://explorer.kstadium.io/"

chromedriver_path = os.getcwd() + '/chromedriver'
driver = webdriver.Chrome(service=Service(chromedriver_path), options=webdriver.ChromeOptions())

search_css_selector = '#root > div.sc-jrQzAO.efokId > main > section.sc-jOxtWs.iJeUrj > div.sc-hmjpVf.ijnNvF > div > form > input'
search_key_word = '0xFc50afdd6db9dE442251f643b6Efb0A1926FE0b5'
click_x_path = '//*[@id="root"]/div[2]/main/section[1]/div[1]/div/form/button'

balance_css_selector = '#root > div > main > section > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(2)'
transaction_click_x_path = '//*[@id="root"]/div/main/section/div/div[1]/button[2]'
transaction_column_css_selector = '#root > div > main > section > div > div:nth-child(3) > table > tbody > tr:nth-child(1)'
contract_column_css_selector = '#root > div > main > section > div > div:nth-child(3) > table > tbody > tr:nth-child(2)'
image_extension = '.png'


def make_csv_file(csv_path, driver, search_key_word):
    """
    :param csv_path: 생성하려는 파일을 담을 디렉토리를 포함한 경로
    :param driver: 기존의 열려있는 크롬 driver
    :param search_key_word: 홈화면에서 찾고자 하는 검색어 중 주소값
    :function : csv_path 에 search_key_word.csv 파일을 이름으로 데이터를 담아서 csv 파일을 생성한다.
    :return: None
    """
    f = open(f'{csv_path}/{search_key_word}.csv', 'w')
    tr = driver.find_elements(By.TAG_NAME, 'tr')
    column = tr[0].text.replace(' ', ',',) + '\n'
    f.write(column)
    for i in range(1, len(tr)):
        sentence = tr[i].text.replace(' ', ',') + '\n'
        f.write(sentence)
    print(f'{search_key_word}.csv 파일이 {csv_path} 경로에 생성되었습니다.')
    f.close()
    return


def put_address(cur_url):
    """
    :param cur_url: 사이트에서 address 가 담긴 url
    :function: 사이트에서 address 가 담긴 페이지로 이동해 address 값을 list 에 추가한다.
    :return: address 값을 담은 리스트
    """
    global driver
    address_arr = []

    driver.get(cur_url)
    sleep(2.5)
    elem = driver.find_elements(By.TAG_NAME, 'tr')
    for i in range(1, len(elem)):
        try:
            _address = elem[i].text.split()[1]
            address_arr.append(_address)
        except ValueError:
            print(f'address 값이 존재하지 않습니다.')
            continue
    return address_arr


def automation_test_3(cur_url, key_word):
    """
    :param cur_url: 홈 url
    :param key_word: 찾으려는 주소 값
    :function: 자동화 테스트 1 수행(검색 후 스크린샷 저장, Balance 데이터 출력, Transaction 관련 데이터 생성 후 저장)
    :return: None
    """
    global driver
    global image_extension
    global search_css_selector
    global click_x_path
    global balance_css_selector
    global transaction_column_css_selector
    global contract_column_css_selector

    folder_path = create_folder('/automation_case_3')
    driver.get(cur_url)
    sleep(2.5)
    elem = driver.find_element(By.CSS_SELECTOR, search_css_selector)
    elem.clear()
    elem.send_keys(key_word)
    driver.find_element('xpath', click_x_path).click()
    sleep(2.5)

    # 예외처리
    string = driver.current_url.split(key_word)[0]
    if string != 'https://explorer.kstadium.io/account/':
        print(f'{key_word}로 검색한 결과가 없습니다.')
        driver.quit()
        return

    screen_image_name = f'{folder_path}/{key_word}{image_extension}'
    el = driver.find_element(By.TAG_NAME, 'body')
    el.screenshot(screen_image_name)

    data = {}
    soup = html_parse(driver)
    balance_tag = soup.select_one(balance_css_selector)
    if balance_tag is None:
        csv_path = create_folder('/automation_case_3_csv')
        make_csv_file(csv_path, driver, key_word)
    else:
        data['Balance'] = balance_tag.text

        driver.find_element('xpath', transaction_click_x_path).click()
        sleep(2.5)
        csv_path = create_folder('/automation_case_3_csv')
        make_csv_file(csv_path, driver, key_word)
        print(f'{search_key_word}: {data}')
    # driver.quit()  # 단독 실행 시 활성화
    return


addresses = put_address('https://explorer.kstadium.io/accounts')

if len(addresses) == 0:
    print(f'주소가 존재하지 않아서 검색을 드라이버를 종료합니다.')
    driver.quit()
else:
    for address in addresses:
        automation_test_3(url, address)
    driver.quit()

# test_key_word = '21a34c702bfe8d06544e557fcc06965a86365933'
# automation_test_3(url, search_key_word)

"""
    여러개의 주소값을 대상으로 자동화 테스트 케이스3을 실행하겠습니다.
"""
