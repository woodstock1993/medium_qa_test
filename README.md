# medium_qa_test

![image](https://user-images.githubusercontent.com/67543838/180643284-a30f3dc0-0d2f-4a01-8b04-07bcc47df41c.png)

# 목차

- [medium 기업과제](#medium_기업과제)
- [과제 해석](#과제-해석)
- [구현 요구사항](#구현-요구사항)


## 과제 해석

자동화 케이스1
- 홈 화면의 Block Height의 값이 Overview 페이지에 잘 반영이 되는지 확인하는 작업

자동화 케이스2
- 최신 블럭 중 Transaction 값이 1이 나올 때 까지 찾는 작업 

자동화 케이스3
- 주소 값 검색 시 Balance 값을 추출하고 Transactions 내 페이지의 데이터를 파일화 하는 작업

## 구현 요구사항
자동화 케이스1
- [x] 홈화면의 블록 값 중 하나를 선택하는 기능
- [x] 특정 블록 페이지로 이동하는 기능
- [x] 해당 페이지의 필요한 값들을 추출하는 기능
- [x] 추출한 값을 파일로 만드는 기능
- [x] 해당 파일을 저장할 폴더를 만드는 기능

자동화 케이스2
- [x] 홈 화면의 Transcations 값을 추출하는 기능
- [x] 추출 한 값 중 1이 있는지 체크하는 기능
- [x] 체크한 페이지에 대해서 스크린 샷을 찍는 기능
- [x] 추출한 값이 없다면 다음페이지로 이동하는 기능
- [x] 추출한 값 중 1이 있으면 화면 캡처 후 종료하는 기능

자동화 케이스3
- [x] 홈 화면에서 주소 값을 검색하는 기능
- [x] 주소 검색 후 해당 페이지에서 캡처 기능 및 Balance 값을 추출하는 기능
- [x] 해당 페이지에서 Transactions 페이지로 이동 후 해당 페이지의 필요한 값을 추출하여 파일화 하는 기능
- [x] 파일을 저장할 폴더를 만들고 파일을 저장하는 기능

### 기술 스택
<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=Python&logoColor=white"/>  <img src="https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=PyCharm&logoColor=white"/> 

### 개발 기간
- 2022.07.20 - 2022.07.25

### Step to run
```
$ https://chromedriver.chromium.org/downloads // 해당 링크로 가서 자신이 사용하는 운영체제와 크롬버전에 맞는 드라이버를 다운로드
$ git clone https://github.com/woodstock1993/medium_qa_test.git // 다운받고자 하는 위치로 이동해서 git clone 실시 후 크롬 드라이버를 git clone 한 위치로 이동시킨다.
$ python -m venv venv
$ pip install --upgrade pip
$ source venv/bin/activate // Mac 명령어
$ .\venv\Scripts\activate  // Window 명령어
$ pip install -r requirements.txt
$ automation_case_1.py // 자동화 케이스 1 실행 
$ automation_case_2.py // 자동화 케이스 2 실행 
$ automation_case_3.py // 자동화 케이스 3 실행 
```
