# 中山大学羽毛球抢场脚本

**背景与初衷**  
尽管我并不打羽毛球，但是我打羽毛球的同学们经常为抢场而苦恼，他们总是抢不到场。我意识到，场肯定都被用脚本抢走了。  
中大的体育场馆预约系统（还有校园网）是出了名的烂，定点放场拼手速的这个机制也给了脚本可乘之机，为了科技平权，我自己写了一份抢场代码，并将其公开。  
显然，这只是权宜之计，如果想要彻底解决这个问题，还是需要校方出手，增加羽毛球场地数量（将排球场的部分时间段改成羽毛球场？），更改抢场机制（比如改成抽签制），加强反爬系统。  
祝愿大家都能打上羽毛球,也祝愿中大越来越好!
  
**脚本环境配置**
>考虑到使用这份脚本的同学，可能并未接触过代码，所以我会讲得稍微详细一点，但是难免有所疏漏，这时就请大家自行deepseek

1、首先，下载一个[Visual Studio Code](https://code.visualstudio.com/)  
2、安装[python3](https://www.python.org/downloads/) ,并将其加入到系统路径中（不同系统此处操作不一样 所以请自行ds）
在mac系统中，可以直接在terminal终端运行以下代码
```
brew install python3
```
3、安装pip3 
4、安装chrome和对应版本的chromedrive（这里需要改成链接） 
5、下载脚本并在vscode中打开 

**脚本参数调整**  
1、需要将options.add_argument("--user-data-dir='/Users/jason/Library/Application Support/Google/Chrome/") 的路径更改为你电脑上的实际路径 
2、需要设置以下参数（每次抢场都要更改） 
<img width="745" alt="image" src="https://github.com/user-attachments/assets/5bcdf45c-477a-4760-b4b7-d3279ab2d38b" />  
3、使用脚本前，需要手动登陆（将这三行代码的#删掉 
<img width="708" alt="image" src="https://github.com/user-attachments/assets/ec485118-4038-4619-ba6a-75d996f86eec" />  
然后在vscode的终端输入   
```
python3 grabBadmintonField.py
```
此时应当跳出浏览器 
然后输入你的netID、密码和验证码 


**在需要抢场之前，启动脚本**  
注意，启动脚本时可以试一下手动登陆的那几行代码，但是正式抢场时，务必将它们变成注释。  
