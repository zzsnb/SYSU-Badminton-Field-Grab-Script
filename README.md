# 中山大学羽毛球抢场脚本

**背景与初衷**  
尽管我并不打羽毛球，但是我打羽毛球的同学们经常为抢场而苦恼，他们总是抢不到场。我意识到，场肯定都被用脚本抢走了。  
中大的体育场馆预约系统（还有校园网）是出了名的烂，定点放场拼手速的这个机制也给了脚本可乘之机，为了科技平权，我自己写了一份抢场代码，并将其公开。  
显然，这只是权宜之计，如果想要彻底解决这个问题，还是需要校方出手，增加羽毛球场地数量（将排球场的部分时间段改成羽毛球场？），更改抢场机制（比如改成抽签制），加强反脚本机制。  
祝愿大家都能打上羽毛球,也祝愿中大越来越好!
  
## 脚本环境配置
> 考虑到使用这份脚本的同学，可能并未接触过代码，所以我会讲得稍微详细一点，但是难免有所疏漏，这时就请大家自行deepseek

### 1. 开发环境准备

#### 1.1 安装代码编辑器
首先，下载并安装[Visual Studio Code](https://code.visualstudio.com/)作为代码编辑器。
- 安装完成后打开VS Code
- 在VS Code中安装Python扩展：点击左侧扩展图标，搜索"Python"并安装

#### 1.2 Python安装指南

**Windows系统：**
- 从[Python官网](https://www.python.org/downloads/)下载最新版本
- 安装时请确保勾选"Add Python to PATH"选项
- 安装完成后，打开命令提示符(cmd)，输入`python --version`验证安装

**macOS系统：**
- 方法1：从[Python官网](https://www.python.org/downloads/)下载macOS安装包
- 方法2（推荐）：使用Homebrew安装
  ```
  brew install python3
  ```
- 验证安装：在Terminal中输入`python3 --version`

**Linux系统：**
- Ubuntu/Debian:
  ```
  sudo apt update
  sudo apt install python3 python3-pip
  ```
- CentOS/RHEL:
  ```
  sudo yum install python3 python3-pip
  ```

#### 1.3 pip3安装与验证

大多数情况下，安装Python3时已经自带pip3。验证方法：
```
pip3 --version
```

如果没有安装pip3：
- **Windows**：重新安装Python并确保选择了pip选项
- **macOS/Linux**：
  ```
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python3 get-pip.py
  ```

#### 1.4 安装必要的Python库
打开终端或命令提示符，运行：
```
pip3 install selenium webdriver-manager schedule
```
系统可能会提示说不允许安装在全局环境下 此时可以开一个venv或conda的虚拟环境  
或者使用以下代码强行安装（不推荐）  
```
pip3 install --user --ignore-installed selenium webdriver-manager schedule
```

### 2. 浏览器与WebDriver配置

#### 2.1 安装Chrome浏览器
如果尚未安装Chrome，请从[官方网站](https://www.google.com/chrome/)下载并安装。

#### 2.2 ChromeDriver安装

**自动安装方式（推荐）：**
脚本中已经整合了webdriver-manager，会自动下载匹配的ChromeDriver。

**手动安装方式：**
1. 检查Chrome版本：打开Chrome，点击右上角三点 > 帮助 > 关于Google Chrome
2. 根据版本号下载对应的[ChromeDriver](https://chromedriver.chromium.org/downloads)
3. 解压下载的文件
4. 将ChromeDriver添加到系统PATH：
   - **Windows**: 将chromedriver.exe复制到Python安装目录
   - **macOS/Linux**: 将chromedriver移动到`/usr/local/bin/`目录

### 3. 脚本配置与使用

#### 3.1 下载脚本
从GitHub仓库下载脚本到本地（只需要下载[grabBadmintonField.py](https://github.com/zzsnb/SYSU-Badminton-Field-Grab-Script/blob/main/grabBadmintonField.py) 即可）。

#### 3.2 配置脚本
在VS Code中打开脚本文件，修改以下关键参数：

1. 修改Chrome用户数据目录路径
   ```python
   options.add_argument("--user-data-dir='你的Chrome用户数据目录路径'")
   ```
   - **Windows路径示例**: `C:\\Users\\用户名\\AppData\\Local\\Google\\Chrome\\User Data`
   - **macOS路径示例**: `/Users/用户名/Library/Application Support/Google/Chrome/`
   - **Linux路径示例**: `/home/用户名/.config/google-chrome/`

2. 设置抢场参数（每次抢场都需更改）
<img width="745" alt="image" src="https://github.com/user-attachments/assets/5bcdf45c-477a-4760-b4b7-d3279ab2d38b" />  

#### 3.3 初次运行与登录
首次使用时，需要手动登录系统：
1. 取消以下三行代码的注释（删除前面的#）
<img width="708" alt="image" src="https://github.com/user-attachments/assets/ec485118-4038-4619-ba6a-75d996f86eec" />

3. 在VS Code终端中运行脚本：
```
python3 grabBadmintonField.py
```
3. 在弹出的浏览器窗口中输入中大NetID、密码和验证码完成登录

#### 3.4 正式抢场
抢场前的准备：
1. 确保已经完成了上述配置
2. **重要**: 将手动登录的代码重新注释掉（前面加上#）
3. 在接近抢场时间前启动脚本
```
python3 grabBadmintonField.py
``` 
正式启动时 脚本的最后几行代码应当是如下状态  
<img width="714" alt="image" src="https://github.com/user-attachments/assets/036a34bb-f569-476a-b560-8bd6083e30c1" />  


### 4. 常见问题与解决方案

1. **ChromeDriver版本不匹配**
   - 错误信息: "session not created: This version of ChromeDriver only supports Chrome version XX"
   - 解决方案: 更新ChromeDriver或Chrome浏览器，确保两者版本匹配

2. **找不到元素**
   - 可能原因: 网页结构变化或加载延迟
   - 解决方案: 检查网站是否更新了界面，或增加等待时间

3. **登录失败**
   - 解决方案: 确认账号密码正确，网络连接稳定，可尝试手动登录再运行脚本

4. **脚本运行后没有反应**
   - 检查Python版本是否正确
   - 确认所有依赖包已安装
   - 检查脚本中的路径配置是否正确

### 5. 注意事项

- 脚本仅供学习和研究使用，如果你真拿去用了，请自负责任
- **_可能导致账号被封禁，甚至被学校处分（网上的通知写得很清楚 会停止账户预订权限一年 且到期后需要提交检讨_**
- 建议在抢场前20分钟启动脚本，不要提前太久
- 只能使用校园网抢场
- 如果有人敢拿这份代码去卖钱 或者提供抢场服务什么的 我只好说 祝你永远杀下网 拍线打一次断一次 睡觉做噩梦 吃饭噎着喉咙  
- 脚本虽好用 但还是建议大家只抢自己需要的场 也不要抢得太多 毕竟打球打太多真的伤身  

---

如有问题或建议，欢迎在Issues中提出，也欢迎Pull Request贡献代码改进!
