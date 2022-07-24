from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
import os


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
        print(f'{path} 경로에 폴더가 생성되었습니다')
    return path


def html_parse(driver):
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    return soup