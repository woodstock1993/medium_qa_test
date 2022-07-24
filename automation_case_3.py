from utils.commons import *
from selenium.webdriver.common.by import By

url = "https://explorer.kstadium.io/"

chromedriver_path = os.getcwd() + '/chromedriver'
driver = webdriver.Chrome(service=Service(chromedriver_path), options=webdriver.ChromeOptions())

search_css_selector = '#root > div.sc-jrQzAO.efokId > main > section.sc-jOxtWs.iJeUrj > div.sc-hmjpVf.ijnNvF > div > form > input'
search_key_word = '0xFc50afdd6db9dE442251f643b6Efb0A1926FE0b5'
click_x_path = '//*[@id="root"]/div[2]/main/section[1]/div[1]/div/form/button'

balance_css_selector = '#root > div > main > section > div > div:nth-child(3) > table > tbody > tr:nth-child(1) > td:nth-child(2)'
transaction_click_x_path = '//*[@id="root"]/div/main/section/div/div[1]/button[2]'
transaction_column_css_selector = '#root > div > main > section > div > div:nth-child(3) > table > tbody > tr:nth-child(1)'

image_extension = '.png'
one_exist = False
number_exist = False


def return_latest_png_number(path_dir):
    """
    :param path_dir: 현재 경로에 덧붙일 폴더(/폴더이름)을 포함한 경로를 적어준다.
    :return: 폴더 내에 숫자만으로 이루어진 이름이 있을 경우 그 중에서 가장 큰 번호를 반환한다. 없을 경우 1을 반환한다.
    """
    global one_exist
    global number_exist

    num_arr = []
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


def automation_test_3(cur_url):
    global driver
    global folder_path
    global png_num
    global image_extension
    global one_exist
    global number_exist
    global search_css_selector
    global search_key_word
    global click_x_path
    global balance_css_selector
    global transaction_column_css_selector

    driver.get(cur_url)
    sleep(2)
    elem = driver.find_element(By.CSS_SELECTOR, search_css_selector)
    elem.clear()
    elem.send_keys(search_key_word)
    driver.find_element('xpath', click_x_path).click()
    sleep(2)
    screen_image_name = f'{folder_path}/{search_key_word}{image_extension}'
    driver.save_screenshot(screen_image_name)

    data = {}
    soup = html_parse(driver)
    balance_tag = soup.select_one(balance_css_selector)
    data['Balance'] = balance_tag.text

    driver.find_element('xpath', transaction_click_x_path).click()
    sleep(2)

    csv_path = create_folder('/automation_case_3_csv')
    f = open(f'{csv_path}/{search_key_word}.csv', 'w')
    tr = driver.find_elements(By.TAG_NAME, 'tr')
    column = tr[0].text.replace(' ', ',',) + '\n'
    f.write(column)
    for i in range(1, len(tr)):
        sentence = tr[i].text.replace(' ', ',') + '\n'
        f.write(sentence)
    f.close()
    driver.quit()
    return


folder_path = create_folder('/automation_case_3')
png_num = return_latest_png_number(folder_path)
automation_test_3(url)
