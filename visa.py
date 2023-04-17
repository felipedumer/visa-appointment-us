# -*- coding: utf8 -*-

import time
import json
import random
import platform
from datetime import datetime

from selenium.webdriver.chrome.service import Service
import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

USERNAME = ''
PASSWORD = ''
SCHEDULE = ''

PUSH_TOKEN = '<my push token>'
PUSH_USER = '<my push user>'

MY_SCHEDULE_DATE = "2023-06-13" # 2020-12-02
#MY_CONDITION = lambda month,day: int(month) == 11 or (int(month) == 12 and int(day) <=5)
MY_CONDITION = lambda month,day: int(month) == 11 and int(day) >= 5

SLEEP_TIME = 120   # recheck time interval

DATE_URL = "https://ais.usvisa-info.com/pt-br/niv/schedule/%s/appointment/days/56.json?appointments[expedite]=false" % SCHEDULE
TIME_URL = "https://ais.usvisa-info.com/pt-br/niv/schedule/%s/appointment/times/56.json?date=%%s&appointments[expedite]=false" % SCHEDULE
APPOINTMENT_URL = "https://ais.usvisa-info.com/pt-br/niv/schedule/%s/appointment" % SCHEDULE
HUB_ADDRESS = 'http://localhost:4444/wd/hub'
EXIT = False


def send(msg):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": '',
        "user": '',
        "message": msg
    }
    requests.post(url, data)


# def get_drive():
    # local_use = platform.system() == 'Darwin'
    # if local_use:
    #     dr = webdriver.Chrome(executable_path = './chromedriver')
    # else:
    #     dr= webdriver.Remote(command_executor=HUB_ADDRESS, desired_capabilities=DesiredCapabilities.CHROME)
    # return dr

    # service = Service(executable_path="./chromedriver")
    # driver = webdriver.Chrome(service=service)

# driver = get_drive()
# service = Service(executable_path=r"C:\Users\felip\Dev\visa\chromedriver\chromedriver.exe")

# driver = webdriver.Chrome(service=service)

# service = ChromeService(executable_path=ChromeDriverManager().install())

# driver = webdriver.Chrome()

driver = webdriver.Edge()

# driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)

def login():
    # Bypass reCAPTCHA
    print("Getting login page")
    driver.get("https://ais.usvisa-info.com/pt-br/niv/users/sign_in")
    print("awaiting 1 sec")
    time.sleep(1)
    print("Get element by xpath")
    # a = driver.find_element_by_xpath('//a[@class="down-arrow bounce"]')
    a = driver.find_element(By.XPATH, '//a[@class="down-arrow bounce"]')
    print("Clicking")
    a.click()
    time.sleep(1)

    print("start sign")
    # href = driver.find_element_by_xpath('//*[@id="header"]/nav/div[2]/div[1]/ul/li[3]/a')
    # href = driver.find_element(By.XPATH, '//*[@id="header"]/nav/div[2]/div[1]/ul/li[3]/a')
    # href.click()
    time.sleep(1)
    Wait(driver, 60).until(EC.presence_of_element_located((By.NAME, "commit")))
    
    print("click bounce")
    # a = driver.find_element_by_xpath('//a[@class="down-arrow bounce"]')
    a = driver.find_element(By.XPATH, '//a[@class="down-arrow bounce"]')
    a.click()
    time.sleep(1)

    do_login_action()


def do_login_action():
    print("input email")
    # user = driver.find_element_by_id('user_email')
    user = driver.find_element(By.ID, 'user_email')
    user.send_keys(USERNAME)
    time.sleep(random.randint(1, 3))

    print("input pwd")
    # pw = driver.find_element_by_id('user_password')
    pw = driver.find_element(By.ID, 'user_password')
    pw.send_keys(PASSWORD) 
    time.sleep(random.randint(1, 3))

    print("click privacy")
    # box = driver.find_element_by_class_name('icheckbox')
    box = driver.find_element(By.CLASS_NAME, 'icheckbox')
    box .click()
    time.sleep(random.randint(1, 3))

    print("commit")
    # btn = driver.find_element_by_name('commit')
    btn = driver.find_element(By.NAME, 'commit')
    btn.click()
    time.sleep(random.randint(1, 3))

    # Wait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Continue')]")))
    Wait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Continuar')]")))
    print("Login successfully! ")


def get_date():
    driver.get(DATE_URL)
    if not is_logined():
        login()
        return get_date()
    else:
        # content = driver.find_element_by_tag_name('pre').text
        content = driver.find_element(By.TAG_NAME, 'pre').text
        date = json.loads(content)
        return date


def get_time(date):
    time_url = TIME_URL % date
    driver.get(time_url)
    # content = driver.find_element_by_tag_name('pre').text
    content = driver.find_element(By.TAG_NAME, 'pre').text
    data = json.loads(content)
    time = data.get("available_times")[-1]
    print("Get time successfully!")
    return time


def reschedule(date):
    global EXIT
    print("Start Reschedule")

    time = get_time(date)
    driver.get(APPOINTMENT_URL)

    data = {
        # "utf8": driver.find_element_by_name('utf8').get_attribute('value'),
        "utf8": driver.find_element(By.NAME, 'utf8').get_attribute('value'),
        # "authenticity_token": driver.find_element_by_name('authenticity_token').get_attribute('value'),
        "authenticity_token": driver.find_element(By.NAME, 'authenticity_token').get_attribute('value'),
        # "confirmed_limit_message": driver.find_element_by_name('confirmed_limit_message').get_attribute('value'),
        "confirmed_limit_message": driver.find_element(By.NAME, 'confirmed_limit_message').get_attribute('value'),
        # "use_consulate_appointment_capacity": driver.find_element_by_name('use_consulate_appointment_capacity').get_attribute('value'),
        "use_consulate_appointment_capacity": driver.find_element(By.NAME, 'use_consulate_appointment_capacity').get_attribute('value'),
        "appointments[consulate_appointment][facility_id]": "56",
        "appointments[consulate_appointment][date]": date,
        "appointments[consulate_appointment][time]": time,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
        "Referer": APPOINTMENT_URL,
        "Cookie": "_yatri_session=" + driver.get_cookie("_yatri_session")["value"]
    }
    
    r = requests.post(APPOINTMENT_URL, headers=headers, data=data)
    if(r.text.find('Successfully Scheduled') != -1):
        print("Successfully Rescheduled")
        send("Successfully Rescheduled")
        EXIT = True
    else:
        print("ReScheduled Fail")
        send("ReScheduled Fail")


def is_logined():
    content = driver.page_source
    if(content.find("error") != -1):
        return False
    return True


def print_date(dates):
    for d in dates:
        print("%s \t business_day: %s" %(d.get('date'), d.get('business_day')))
    print()


last_seen = None
def get_available_date(dates):
    global last_seen

    def is_earlier(date):
        return datetime.strptime(MY_SCHEDULE_DATE, "%Y-%m-%d") > datetime.strptime(date, "%Y-%m-%d")

    for d in dates:
        date = d.get('date')
        if is_earlier(date) and date != last_seen:
            # _, month, day = date.split('-')
            # if(MY_CONDITION(month, day)):
                # last_seen = date
                # return date
            last_seen = date
            return date


def push_notification(dates):
    msg = "date: "
    for d in dates:
        msg = msg + d.get('date') + '; '
    send(msg)


if __name__ == "__main__":
    login()
    retry_count = 0
    while 1:
        if retry_count > 6:
            break
        try:
            print(datetime.today())
            print("------------------")

            dates = get_date()[:5]
            print_date(dates)
            date = get_available_date(dates)
            if date:
                print("\033[31m DATE AVAILABLE, RESCHEDULE NOW!!!")
                print("\033[31m DATE AVAILABLE, RESCHEDULE NOW!!!")
                print("\033[31m DATE AVAILABLE, RESCHEDULE NOW!!!")
                print("\033[31m DATE AVAILABLE, RESCHEDULE NOW!!!")
                print("\033[31m DATE AVAILABLE, RESCHEDULE NOW!!!")
                print("\033[31m DATE AVAILABLE, RESCHEDULE NOW!!!")
                print("\033[31m DATE AVAILABLE, RESCHEDULE NOW!!!")
                print("\033[31m DATE AVAILABLE, RESCHEDULE NOW!!!")
                push_notification(dates)
                # reschedule(date)

            if(EXIT):
                break

            time.sleep(SLEEP_TIME)
        except:
            retry_count += 1
            time.sleep(60*5)
    
    if(not EXIT):
        send("HELP! Crashed.")