from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
import time
import schedule
import random



# !!! 这里需要你修改配置
bookDate = "05-15"
bookTime1 = 19
bookTime2 = 20
# 如果要选8:00-9:00的场 就写8 如果要选21:00 - 22:00 的场 就写21
bookCampus = "east" 
# 东校 - east 南校 - south 北校 - north 深圳 - shenzhen 珠海 - zhuhai
bookField = 6 # 首选场，这里填入整数 不要加双引号！
fallbackField1 = 2 # 备选场1，这里填入整数 不要加双引号！
fallbackField2 = 7 # 备选场2，这里填入整数 不要加双引号！
fallbackField3 = 9 # 备选场2，这里填入整数 不要加双引号！
# 东校有14个场 南校有 个场 深圳有12个场 珠海有10个场
# 但是由于东校的场地11是不存在的 所以当你抢东校12/13/14号场时 请自动-1 输入成11/12/13
waitTimeForShow = 0 # 正式使用时 请把这个调整成0 如果想要看抢场的过程 可以调成2或3
# !!!!!!

waitTimeChangeField = 1

switch_dict = {
    "south": "广州校区南校园",
    "east": "广州校区东校园",
    "north": "广州校区北校园",
    "shenzhen": "深圳校区",
    "zhuhai": "珠海校区"
}
if bookCampus not in switch_dict:
    raise ValueError(f"无效校区: {bookCampus}。可选: {list(switch_dict.keys())}")
campusName = switch_dict[bookCampus]

switch_dict2 = {
    "south": "南校园新体育馆羽毛球场（学生）",
    "east": "东校园体育馆羽毛球场",
    "north": "北校园体育馆羽毛球场（学生）",
    "shenzhen": "深圳校区羽毛球场",
    "zhuhai": "珠海校区新体育馆羽毛球场"
}
gymName = switch_dict2[bookCampus]

time_map = {
    8: 1,    # 08:00-09:00 → tr[1]
    9: 2,     # 09:00-10:00 → tr[2]
    10: 3,    # 10:00-11:00 → tr[3]
    11: 4,    # 11:00-12:00 → tr[4]
    14: 5,    # 14:00-15:00 → tr[5]
    15: 6,    # 15:00-16:00 → tr[6]
    16: 7,    # 16:00-17:00 → tr[7]
    17: 8,    # 17:00-18:00 → tr[8]
    18: 9,    # 18:00-19:00 → tr[9]
    19: 10,   # 19:00-20:00 → tr[10]
    20: 11,   # 20:00-21:00 → tr[11]
    21: 12    # 21:00-22:00 → tr[12]
}
field_map = {
    1: 2,     # 场地1 → td[2]
    2: 3,     # 场地2 → td[3]
    3: 4,     # 场地3 → td[4]
    4: 5,     # 场地4 → td[5]
    5: 6,     # 场地5 → td[6]
    6: 7,     # 场地6 → td[7]
    7: 8,     # 场地7 → td[8]
    8: 9,     # 场地8 → td[9]
    9: 10,    # 场地9 → td[10]
    10: 11,   # 场地10 → td[11]
    11: 12,   # 场地11 → td[12]
    12: 13,   # 场地12 → td[13]
    13: 14,   # 场地13 → td[14]
    14: 15    # 场地14 → td[15]
}
timeName1 = time_map[bookTime1]
timeName2 = time_map[bookTime2]
fieldName = field_map[bookField]


# 请下载好和电脑上chrome版本对应的chromedriver 并将其添加到PATH上（这一段请自行deepseek）
# 下面这一段是配置chromedriver 
# 为了不用输入验证码（需要识别文字）所以使用登陆时已经保持的状态。

options = webdriver.ChromeOptions()


# !!!!!!这一部分需要你配置!!!!
options.add_argument("--user-data-dir='/Users/jason/Library/Application Support/Google/Chrome/") 
# !!!!!这里要替换为你电脑上chrome用户数据目录的实际路径!!!!!
# mac上往往就是我上面这个链接 但是还是最好用访达的"command+shift+g"确认一下那里是不是有这个文件
# 在mac上，对一个文件右键后按住option键，会发现复制按钮变成了复制路径
# !!!!!!


options.add_argument("--profile-directory=Default")  # 使用默认配置（如果有多个配置需指定）
# 尽量不要让浏览器知道自己在被自动化控制
options.add_argument("--start-maximized")
# 最大化窗口
options.add_argument("--disable-extensions")
# 禁用窗口
options.add_argument("--disable-gpu")
# 禁用GPU加速
options.add_experimental_option("excludeSwitches", ["enable-automation"])
# 隐藏自动化特征

# 启动！
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome(service=service) # 如果指定了路径

def login(driver):
    # 理论上 这里不需要输入密码和验证码 直接就可以进
    # 但由于网站对身份验证系统有定时机制 需要在抢场前 先手动登陆
    # 当然 这部分可以开发成ai识图
    driver.get("https://gym.sysu.edu.cn/#/") 
    print("浏览器已成功打开 中山大学体育预约平台 首页！")
    time.sleep(waitTimeForShow)
    driver.refresh()


def lead_to_place(driver):
    def close_swimming_message(driver):
        try:
            booking_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='关闭']")))  
            booking_button.click()
            print("关闭游泳通知")
            time.sleep(waitTimeForShow)
        except Exception as e:
            print(f"游泳通知关闭点击失败: {str(e)}")


    def choose_campus(driver):
        try:
            # 这里图片只是一个幌子 实际上点击的是上面覆盖的隐藏组件
            xpath = f"//h3[contains(text(), '{campusName}')]/ancestor::div[@class='campus-card']"
            campus_card = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            campus_card.click()
            print(f"成功点击{campusName}")
            time.sleep(waitTimeForShow)
        except Exception as e:
            print(f"校园选择点击失败: {str(e)}")
    
    def choose_gym(driver):
        try:
            xpath = f"//h3[@class='facility-name' and text()='{gymName}']/ancestor::div[@class='facility-card']"
            facility_card = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
            )
            facility_card.click()
            print(f"成功点击{gymName}")
            time.sleep(waitTimeForShow)
        except Exception as e:
            print(f"场馆选择点击失败: {str(e)}")

    close_swimming_message(driver)
    choose_campus(driver)
    choose_gym(driver)

def book(driver):
    def choose_date(driver):
        while True:
            try:
                date_xpath = f"//div[@class='date-number' and text()='{bookDate}']/ancestor::div[@class='date-item']"
                # 随机延迟10~50毫秒 + 1秒 （怕系统觉得我手速太快了 但又不想系统发现我每次刷新的间隔都一样
                delay_ms = random.randint(10, 50) / 1000.0
                date_item = WebDriverWait(driver, 1 + delay_ms).until(
                    # 这里的刷新机制可能需要更加激进 比如2秒刷新一次？
                    EC.element_to_be_clickable((By.XPATH, date_xpath))
                )
                date_item.click()
                print(f"成功点击{bookDate}")
                break  # 成功后退出循环

            except TimeoutException:
                print("找不到日期，加载失败，刷新页面重试")
                driver.refresh()
                # 随机延迟50~100毫秒（根据系统容忍度调整）
                delay_ms = random.randint(30, 100) / 1000.0
                time.sleep(delay_ms)

    def choose_field_time(driver):
        fieldChoice = fieldName # 新建fieldChoice这个变量是为了能够使用备选方案。
        while True:
            try:
                play_button = WebDriverWait(driver, waitTimeChangeField).until(
                    EC.element_to_be_clickable((
                        # By.XPATH, "//*[@id='app']/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[8]/button"    #这是预约其他场和其他时间的代码，根据这个确定预约时间.第12行代表21-22点，第8列代表第14个场
                        # By.XPATH, "/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[11]/td[9]/button"    # 这是预约其他场和其他时间的代码，根据这个确定预约时间.第2行代表9-10点，第10列代表第16个场
                        # By.XPATH, "/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[10]/button"
                        By.XPATH, f"/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[{timeName1}]/td[{fieldChoice}]/button"   #这里对应东校的场地tr[11]/td[9]代表时间20-21，场地8
                    ))
                )
                play_button.click()
                play_button = WebDriverWait(driver, waitTimeChangeField).until(
                    EC.element_to_be_clickable((
                        # By.XPATH, "//*[@id='app']/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[8]/button"    #这是预约其他场和其他时间的代码，根据这个确定预约时间.第12行代表21-22点，第8列代表第14个场
                        # By.XPATH, "/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[11]/td[9]/button"    # 这是预约其他场和其他时间的代码，根据这个确定预约时间.第2行代表9-10点，第10列代表第16个场
                        # By.XPATH, "/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[1]/td[10]/button"
                        By.XPATH, f"/html/body/div/div/div[2]/main/div/div[2]/div[1]/div[4]/table/tbody/tr[{timeName2}]/td[{fieldChoice}]/button"   #这里对应东校的场地tr[11]/td[9]代表时间20-21，场地8
                    ))
                )
                play_button.click()
                print("两个场点击成功")
                break
            except TimeoutException:
                print("未找时段场馆按钮，可能预约时间未开放")
                # 这里增加了一个机制 当找不到这个按钮的时候 自动改成备选的场号
                if fieldChoice == fieldName:
                    fieldChoice = fallbackField1
                elif fieldChoice == fallbackField1:
                    fieldChoice = fallbackField2
                elif fieldChoice == fallbackField2:
                    fieldChoice = fallbackField3

            
            
    def grab(driver):
        try:
            finbook_button = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, "//*[text()='预约 ']"))
            )
            finbook_button.click()
            print("两个场预约成功！")
            global done 
            done = True
            time.sleep(10)
        except TimeoutException:
            print("未找到预约按钮，可能预约时间未开放")
            # 这里并没有增加失败改用备选方案的机制 或许如果在点击“预约”之后 发现还是不行
            # 这就需要自动关掉通知 然后换用备选方案再抢一次

    driver.refresh() # 到点了需要先refresh一次
    choose_date(driver)
    choose_field_time(driver)
    grab(driver)


# 下面这几行是手动测试的代码 抢场前务必先手动测试 并输入该输入的netID、密码和验证码
# login(driver)
# lead_to_place(driver)
# book(driver)

# 下面这几行是定时抢场操作 使用时务必用"#"将手动测试代码设置为注释
done = False

schedule.every().day.at("21:55").do(login,driver=driver)
schedule.every().day.at("21:57").do(lead_to_place,driver=driver) 
schedule.every().day.at("21:59:59").do(book,driver=driver) # 提前1s刷新 每隔1.0xs再次刷新

while not done:
   schedule.run_pending()