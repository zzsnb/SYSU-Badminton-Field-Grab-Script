
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import schedule
from PIL import Image
from aip import AipOcr
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
from datetime import datetime, timedelta
import os

BASE_DIR = Path(__file__).parent.resolve()  #获取相对路径

# ChromeDriver 路径 下载与当前谷歌浏览器版本适配的Chromedriver并配置
chrome_driver_path = "chromedriver-win64/chromedriver-win64/chromedriver.exe"    #不理解为什么相对路径会有问题
# chrome_driver_path = "C:/Users/1/Desktop/code/chromedriver-win64/chromedriver-win64/chromedriver.exe"  # 替换为实际路径
chrome_binary_path = "chrome-win64/chrome.exe"

# Chrome 启动配置
options = Options()
options.binary_location = chrome_binary_path


options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")  # ------禁用扩展
options.add_argument("--disable-gpu")  # ------禁用 GPU 加速
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # ------减少浏览器检测到 Selenium 控制的可能性
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
# ------尽量不要让浏览器感知自己在被自动化控制：禁用扩展、禁用 GPU 加速、某个开关
# print(driver.capabilities['browserVersion'])  # 输出 Chrome 版本
# print(driver.capabilities['chrome']['chromedriverVersion'])  # 输出 ChromeDriver 版本



screenshotadd = "screenshot/screenshot.png"
codeadd = "screenshot/code.png"
netid = ''
password = ''
bookdate = "04-22"
waittime_1 = 30
waittime_2 = 40    #after button 南校园学生场（时间秒）
waittime_3 = 40    #after button 日期
waittime_4 = 40    #选好场地后等待预约按键
# playtime = "21:00-22:00"


config = {
        'appId': '',
        'apiKey': '',
        'secretKey': ''
    }#高精度版
# 百度智能识别api注册

client = AipOcr(**config)

def login(driver):
    # global driver
    time.sleep(2)
    driver.get("https://tiyu.sysu.edu.cn")
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[text()='体育场馆管理与预订系统']"))
    )
    # 点击元素
    button.click()
    # 获取当前窗口句柄
    current_window = driver.current_window_handle
    # 获取所有其他窗口句柄
    new_windows = [window for window in driver.window_handles if window != current_window]
    # 切换到新窗口（假设只有一个新窗口）
    if new_windows:
        driver.switch_to.window(new_windows[0])
    time.sleep(1)
    # time.sleep(2)
    print("当前页面网址:", driver.current_url)

    
    username_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='username']")))

    driver.save_screenshot(screenshotadd)
    # time.sleep(1)
    username_input.send_keys(netid)

    # 输入密码
    password_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='password']")))
    password_input.send_keys(password)
    # time.sleep(1)

    imglocation = "//img[@name='captchaImg']"
    im = Image.open(screenshotadd)
    k = 1  # 缩放率
    left = driver.find_element(By.XPATH, imglocation).location['x']
    top = driver.find_element(By.XPATH, imglocation).location['y']
    right = driver.find_element(By.XPATH, imglocation).location['x'] + driver.find_element(By.XPATH, imglocation).size[
        'width']
    bottom = driver.find_element(By.XPATH, imglocation).location['y'] + driver.find_element(By.XPATH, imglocation).size[
        'height']
    im = im.crop((left * k, top * k, right * k, bottom * k))
    im.save(codeadd)

    def img_to_str(image_path):
        identicode = ""
        image = open(image_path, 'rb').read()
        result = client.basicAccurate(image)
        print("OCR API 返回结果：", result)
        if 'words_result' in result:
            with open("result.txt", "a") as f:
                for line in result["words_result"]:
                    identicode = identicode + line["words"]
                    f.write(line["words"] + "\n")
        else:
            print("OCR识别结果中没有 'words_result' 字段。可能是请求失败。")
        return identicode

    def getidentify(image):
        identicode = img_to_str(image)
        return identicode

    txtcode = getidentify(codeadd)
    txtcode = txtcode.replace(" ", "")
    txtcode = txtcode[:4]
    print("验证码是：", txtcode)

    txtcode_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='captcha']")))
    txtcode_input.send_keys(txtcode)
    # time.sleep(1)

    login_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit']")))
    login_button.click()
    # time.sleep(1)

    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//*[contains(text(),'验证码不正确')]")))
        print("验证码错误")
        return False
    except TimeoutException:
        print("登录成功！")
        booking_button = WebDriverWait(driver, 5).until(
            # EC.element_to_be_clickable((By.XPATH, "//*[text()='广州校区南校园 ']")))
            EC.element_to_be_clickable((By.XPATH, "//button[text()='关闭']")))  
        booking_button.click()
        print("关闭游泳通知")
        booking_button = WebDriverWait(driver, 10).until(
            # EC.element_to_be_clickable((By.XPATH, "//*[text()='广州校区南校园 ']")))
            EC.element_to_be_clickable((By.XPATH, "//*[text()='广州校区东校园 ']")))
        booking_button.click()
        return True

def login_untilsuccess():
    global driver
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    result = login(driver)
    while not result:
        time.sleep(1)
        driver.quit()
        print("登录失败退出重新登录")
        time.sleep(1)
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
        result = login(driver)

    print("登录进入南校园or其他校区成功")


def job1():
    global driver
    global bookdate
    # driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    # bad_button = WebDriverWait(driver, waittime_1).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='南校园新体育馆羽毛球场（学生）']")))
    bad_button = WebDriverWait(driver, waittime_1).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='东校园体育馆羽毛球场']")))
    bad_button.click()
    print("点击南校or其他校区羽毛球场")
    time.sleep(1)
    driver.refresh()
    while True:
        try:
            print("当前预约日期:", bookdate)
            datetime = f"//*[text()='{bookdate}']"
            date_button = WebDriverWait(driver, waittime_2).until(EC.element_to_be_clickable((By.XPATH, datetime)))
            date_button.click()
            print("点击日期成功")
                # time.sleep(2)
            break  # 成功后退出循环

        except TimeoutException:
            print("找不到日期，加载失败，刷新页面重试")
            driver.refresh()
    try:
        play_button = WebDriverWait(driver, waittime_3).until(
            EC.element_to_be_clickable((
                # By.XPATH, "//*[@id='app']/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[8]/button"    #这是预约其他场和其他时间的代码，根据这个确定预约时间.第12行代表21-22点，第8列代表第14个场
                # By.XPATH, "/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[11]/td[9]/button"    # 这是预约其他场和其他时间的代码，根据这个确定预约时间.第2行代表9-10点，第10列代表第16个场
                # By.XPATH, "/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[10]/button"
                By.XPATH, "/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[11]/td[9]/button"   #这里对应东校的场地tr[11]/td[9]代表时间20-21，场地8
            ))
        )
        play_button.click()
        print("点击时间和场地成功")
# 如果想预约其他场，根据时间排列顺序调整tr后的数字，根据场地调整td后的数字

        finbook_button = WebDriverWait(driver, waittime_4).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='预约 ']"))
        )
        finbook_button.click()

        print("第一个场点击预约成功")

        schedule.clear()

    except TimeoutException:
        print("未找到时间段或预约按钮，可能预约时间未开放")

    global done
    done = True

def getbookdate():
    global bookdate
    current_datetime = datetime.now().date()
    bookdatetime = current_datetime + timedelta(days=3)
    # formatted_date = current_datetime.strftime("%m-%d")
    
    bookdate = bookdatetime.strftime("%m-%d")
    print("格式化日期:", bookdate)
 

done = False
# 安排# 安排任务
os.system('cls')  # 清除终端信息
# getbookdate()
# print("bookdate:",bookdate)
# login_untilsuccess()
# job1()
schedule.every().day.at("21:40").do(getbookdate)
schedule.every().day.at("21:50").do(login_untilsuccess) 
schedule.every().day.at("22:00").do(job1)     #这应该是一行调开始抢场时间的代码


while not done:
    schedule.run_pending()


