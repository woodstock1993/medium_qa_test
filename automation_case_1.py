from utils.commons import *
import random, re


url = "https://explorer.kstadium.io/"
block_height_css_selector = '#root > div.sc-jrQzAO.efokId > main > section.sc-fFeiMQ.hXmHOb > div > div:nth-child(2) > table > tbody > tr > td > a'
block_height_css_selector_2 = '#root > div > main > section > div > div > div.sc-Galmp.dlSKE > table > tbody > tr > td'
chromedriver_path = os.getcwd() + '/chromedriver'

driver = webdriver.Chrome(service=Service(chromedriver_path), options=webdriver.ChromeOptions())


def trim_data(data, block_num):
    """
    :param data: block 정보를 가진 dict 형태의 데이터
    :param block_num: 블록번호
    :return: 데이터를 전처리 한 후 data를 반환한다.
    """
    for k, v in data.items():
        try:
            if k == 'Timestamp':
                data['Timestamp'] = re.split('[()]', v)[1]
            elif k == 'Transactions':
                data['Transactions'] = v.split()[0]
        except TypeError:
            print(f'block_height {block_num}의 속성 중 {k}가 가지고 있는 값의 형태가 변경되었습니다.')
    return data


def write_file(dir_path, block_num, data):
    """
    :param dir_path: .txt 파일을 쓸 경로 입력
    :param block_num: 블록 번호
    :param data: 블록과 관련한 데이터가 담긴 딕셔너리 형태의 data
    :function: 입력한 경로 폴더에 블록이름.txt 파일을 생성, 해당 파일에는 블록 정보가 담겨있다.
    :return: None
    """
    path = f'{dir_path}/{block_num}.txt'
    f = open(path, 'w')

    for k, v in data.items():
        if k == 'Block Height':
            sentence = f'Block Height: {v}\n'
            f.write(sentence)
        elif k == 'Timestamp':
            sentence = f'Timestamp: {v}\n'
            f.write(sentence)
        elif k == 'Transactions':
            sentence = f'Transactions: {v}\n'
            f.write(sentence)
        elif k == 'Block Reward':
            sentence = f'Block Reward: {v}\n'
            f.write(sentence)
    print(f'{block_num}.txt 파일이 {dir_path} 경로에 생성되었습니다.')
    f.close()
    return


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

    driver.get(cur_url)
    sleep(2.5)
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
        block_height_arr[-1]
    except TypeError:
        print(f'추출된 번호가 단 한개도 없습니다. 자동화 테스트1을 종료합니다.')
        driver.quit()
        return

    try:
        block_height_number = random.choice(block_height_arr)
        print(f'block height 번호: {block_height_number}가 추출되었습니다.')
    except ValueError:
        print(f'추출된 block height 번호가 없거나 block_height_css_selector 가 잘못 설정되었습니다.')
        driver.quit()
        return

    driver.find_element(By.LINK_TEXT, str(block_height_number)).click()
    print(f'block height 번호: {block_height_number}가 클릭되었습니다.')
    sleep(2.5)

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
    else:
        print(f'{block_height_number}가 페이지 속 {cmp_block_height_number}번호와 불일치합니다.')

    data = trim_data(data, block_height_number)
    write_file(folder_path, block_height_number, data)
    print(f'{block_height_number}의 상세정보는 다음과 같습니다, {data}')
    driver.quit()
    return data


folder_path = create_folder('/automation_case_1')
automation_test_2(url)
