from utils.commons import *
from selenium.webdriver.common.by import By

url = "https://explorer.kstadium.io/"

chromedriver_path = os.getcwd() + '/chromedriver'
driver = webdriver.Chrome(service=Service(chromedriver_path), options=webdriver.ChromeOptions())

search_css_selector = '#root > div.sc-jrQzAO.efokId > main > section.sc-jOxtWs.iJeUrj > div.sc-hmjpVf.ijnNvF > div > form > input'
search_key_word = '0xFc50afdd6db9dE442251f643b6Efb0A1926FE0b5'
click_x_path = '//*[@id="root"]/div[2]/main/section[1]/div[1]/div/form/button/img'

balance_css_selector = '#root > div > main > section > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(2)'
transaction_click_x_path = '//*[@id="root"]/div/main/section/div/div[1]/button[2]'
transaction_column_css_selector = '#root > div > main > section > div > div:nth-child(3) > table > tbody > tr:nth-child(1)'
contract_column_css_selector = '#root > div > main > section > div > div:nth-child(3) > table > tbody > tr:nth-child(2)'
image_extension = '.png'


def make_csv_file(csv_path, driver, search_key_word):
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
    global driver
    address_arr = []

    driver.get(cur_url)
    sleep(2)
    elem = driver.find_elements(By.TAG_NAME, 'tr')
    for i in range(1, len(elem)):
        try:
            address = elem[i].text.split()[1]
            address_arr.append(address)
        except ValueError:
            print(f'address 값이 존재하지 않습니다.')
            continue
    return address_arr


def automation_test_3(cur_url, key_word):
    global driver
    global image_extension
    global search_css_selector
    global click_x_path
    global balance_css_selector
    global transaction_column_css_selector
    global contract_column_css_selector

    folder_path = create_folder('/automation_case_3')
    driver.get(cur_url)
    sleep(2)
    elem = driver.find_element(By.CSS_SELECTOR, search_css_selector)
    elem.clear()
    elem.send_keys(key_word)
    driver.find_element('xpath', click_x_path).click()
    sleep(2)

    # 예외처리
    string = driver.current_url.split(key_word)[0]
    if string != 'https://explorer.kstadium.io/account/':
        print(f'{key_word}로 검색한 결과가 없습니다.')
        driver.quit()
        return

    screen_image_name = f'{folder_path}/{key_word}{image_extension}'
    driver.save_screenshot(screen_image_name)

    data = {}
    soup = html_parse(driver)
    balance_tag = soup.select_one(balance_css_selector)
    if balance_tag is None:
        csv_path = create_folder('/automation_case_3_csv')
        make_csv_file(csv_path, driver, key_word)
    else:
        data['Balance'] = balance_tag.text

        driver.find_element('xpath', transaction_click_x_path).click()
        sleep(2)
        csv_path = create_folder('/automation_case_3_csv')
        make_csv_file(csv_path, driver, key_word)
        print(f'{search_key_word}: {data}')
    # driver.quit()
    return


address_arr = put_address('https://explorer.kstadium.io/accounts')
if len(address_arr) == 0:
    print(f'주소가 존재하지 않아서 검색을 드라이버를 종료합니다.')
    driver.quit()
else:
    for address in address_arr:
        automation_test_3(url, address)
    driver.quit()

