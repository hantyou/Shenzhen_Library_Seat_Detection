# Shenzhen_Library_Seat_Detection
深圳图书馆预约空位检测程序，现在支持福田图书馆和深圳图书馆。需要自己进行浏览器配置文件的定位，如果需要发送邮件也需要自己在代码中配置
-   **起因**

    因为早8点图书馆抢位置起不来，而且几分钟内位置就全无了，所以总是预约不到深图和福图的位置，就突击了一下python里面的selenium库，写了一个自动预约程序，借着不想写毕业论文划水的空隙不断增删，目前实现了以下功能：

1.  选择预约日期，支持选择今天或者明天；

2.  选择图书馆，支持深圳图书馆和福田图书馆；

3.  程序开始时手动输入读者证和密码；

4.  支持自动登录、监测指定日期座位、填写健康申报表和发送验证码；

5.  验证码发送后弹窗，输入验证码后点击确认自动将验证码输入到网站上并预约

-   **预设置**

    1. 在系统变量中加入Firefox的路径，例如：

C:\\Program Files\\Mozilla Firefox

    2. 需要一些包：

> pip install -i https://mirrors.aliyun.com/pypi/simple/ selenium\
> pip install -i https://mirrors.aliyun.com/pypi/simple/ win10toast

    3. 可以写一个.bat文件放桌面上，方便双击执行程序：

> d:\
> cd D:\\Programming\\Python\\urllib\
> python LibDetect.py

-   **程序块**

    1. import部分

> \# coding=utf-8\
> from selenium import webdriver\
> import time\
> import tkinter as tk\
> from tkinter import messagebox\
> import datetime\
> import smtplib\
> from email.mime.text import MIMEText\
> \# email 用于构建邮件内容\
> from email.header import Header\
> from win10toast import ToastNotifier\
> from multiprocessing import Process\
> toaster = ToastNotifier()\
> VarValue = \'\'

    2. 监测程序 LibSeatDetect

> def LibSeatDetect(UN, PW, textdate, Libname=\"ShenZhen\",\
>                   webSite=\"https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Factivity\_appt.jsp%3FcategoryId%3D81\"):\
>     \# 配置文件地址\
>     print(Libname + \"图书馆的位置检测已经开始\")\
>     global VarValue\
>     toaster.show\_toast(\"LibDectec Running of \" + Libname + \"Library\",\
>                        \"Script screening library seat of \" + Libname + \" library is running\",\
>                        icon\_path=None,\
>                        duration=20,\
>                        threaded=True)\
>     while toaster.notification\_active(): time.sleep(0.1)\
>     profile\_directory = r\'C:\\Users\\Daniel Zhai\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\sgjgzcra.default\'\
>     \# 加载配置配置\
>     profile = webdriver.FirefoxProfile(profile\_directory)\
>     \# 启动浏览器配置\
>     drive = webdriver.Firefox(profile)\
>     drive.get(webSite)\
>     url = drive.current\_window\_handle\
>     drive.switch\_to.window(url)\
>     name = UN\
>     password = PW\
>     print(\"正在登陆\" + Libname + \"图书馆，账号：\" + name + \"\\n密码：\" + password)\
>     drive.find\_element\_by\_name(\"username\").clear()\
>     drive.find\_element\_by\_name(\"username\").send\_keys(name)\
>     drive.find\_element\_by\_name(\"password\").clear()\
>     drive.find\_element\_by\_name(\"password\").send\_keys(password)\
>     drive.find\_element\_by\_class\_name(\"submit\").click()\
>     SentEmail = False\
>     failCount = 0\
>     print(\"开始检测此日期的座位 \" + textdate)\
> \
>     while 1:\
>         failCount += 1\
>         \"\"\"检测当前监控的位置是否可以预约\"\"\"\
>         if not drive.find\_element\_by\_xpath(\
>                 \"//span\[contains(text(),\" + textdate + \")\]/following-sibling::a\").text == u\"去预约\":\
>             pass\
>         else:\
>             print(\'\\033\[32m有空位\[30m\')\
>             date = datetime.datetime.now()\
>             dateText = str(date.year) + r\'-\' + str(date.month) + r\'-\' + str(date.day) + r\'-\' + str(\
>                 date.hour) + \':\' + str(\
>                 date.minute) + \':\' + str(date.second)\
>             print(dateText)\
>             \"\"\"进入预约界面\"\"\"\
>             if drive.find\_element\_by\_xpath(\
>                 \"//span\[contains(text(),\" + textdate + \")\]/following-sibling::a\").text == u\"去预约\":\
>                 yuyue = drive.find\_element\_by\_xpath(\
>                     \"//span\[contains(text(),\" + textdate + \")\]/following-sibling::a\")\
>                 drive.execute\_script(\"arguments\[0\].scrollIntoView();\", yuyue)\
>                 yuyue.click()\
>             \"\"\"检测是否需要填写健康信息\"\"\"\
>             if u\"请填写您的健康信息\" in drive.page\_source:\
>                 drive.find\_element\_by\_xpath(\
>                     \"/html/body/div\[1\]/div\[2\]/div\[2\]/form/div/div/div/div/div\[1\]/div\[2\]/input\[2\]\").click()\
>                 drive.find\_element\_by\_xpath(\
>                     \"/html/body/div\[1\]/div\[2\]/div\[2\]/form/div/div/div/div/div\[2\]/div\[2\]/input\[2\]\").click()\
>                 known = drive.find\_element\_by\_xpath(\"//\*\[\@id=\'c1\'\]\")\
>                 if not known.is\_selected():\
>                     known.click()\
>                 drive.find\_element\_by\_class\_name(\"page\_btn\").click()\
>                 time.sleep(1)\
>                 try:\
>                     dialog\_box = drive.switch\_to.alert\
>                     print(dialog\_box.text)\
>                     dialog\_box.accept()\
>                 except:\
>                     LibSeatDetect(UN, PW, textdate, Libname, webSite)\
>                     break\
>             \"\"\"进入预约信息填写界面\"\"\"\
>             drive.find\_element\_by\_id(\"getCheckCode\").click()\
>             \"\"\"在预约前发送邮件通知\"\"\"\
>             if not SentEmail:\
>                 try:\
>                     sendAnEmail(dateText, textdate, Libname)\
>                 except:\
>                     print(\"发送邮件失败，跳过\")\
>                     pass\
>             \"\"\"跳出验证码填写界面\"\"\"\
>             app = MyCollectApp()\
>             app.mainloop()\
>             print(VarValue)\
>             \"\"\"请求验证码\"\"\"\
>             drive.find\_element\_by\_css\_selector(\"\[class=\'input w\_small required\'\]\").click()\
>             drive.find\_element\_by\_css\_selector(\"\[name=\'applyCheckCode\'\]\").send\_keys(VarValue)\
>             drive.find\_element\_by\_css\_selector(\"\[class=\'submit btn\_2\'\]\").click()\
>             break\
>         \"\"\"隔一段时间再刷新\"\"\"\
>         if failCount \< 10:\
>             refreshInter = 5\
>             for i in range(1, refreshInter + 1):\
>                 time.sleep(0.999)\
>                 last\_time = refreshInter + 1 - i\
>                 print(\'\\rNo Seat in \' + Libname + \' library, temporarily stop detection for %s seconds.\' % last\_time,\
>                       end=\"\")\
>         else:\
>             LongStopInter = 120\
>             for i in range(1, LongStopInter + 1):\
>                 time.sleep(0.999)\
>                 last\_time = LongStopInter + 1 - i\
>                 print(\
>                     \'\\rNo Seat in \' + Libname + \' library for a long time, temporarily stop detection for %s seconds.\' % last\_time,\
>                     end=\"\")\
>             failCount = 0\
>         drive.refresh()\
>     time.sleep(1)\
>     drive.quit()\
>     quit()

    3. 验证码弹窗类 MyCollectApp

> class MyCollectApp(tk.Toplevel):  \# 重点\
>     def \_\_init\_\_(self):\
>         super().\_\_init\_\_()  \# 重点\
>         self.setupUI()\
>         self.title(\'验证码\')\
> \
>     def setupUI(self):\
>         row1 = tk.Frame(self)\
>         row1.pack(fill=\"x\")\
>         l1 = tk.Label(row1, text=\"验证码：\", height=2, width=10)\
>         l1.pack(side=tk.LEFT)  \# 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM\
>         self.xls\_text = tk.StringVar()\
>         tk.Entry(row1, textvariable=self.xls\_text).pack(side=tk.RIGHT)\
> \
>         row2 = tk.Frame(self)\
>         row2.pack(fill=\"x\")\
>         tk.Button(row2, text=\"点击确认\", command=self.on\_click).pack(side=tk.RIGHT)\
> \
>     def on\_click(self):\
>         global VarValue\
>         VarValue = self.xls\_text.get().lstrip()\
>         if len(VarValue) == 0:\
>             messagebox.showwarning(title=\'系统提示\', message=\'请输入验证码!\')\
>             return False\
> \
>         self.quit()\
>         self.destroy()

    4. 邮件发送函数  sendAnEmail

        此函数如果执行产生任何失败，可以被自动跳过。

> def sendAnEmail(dateText, textdate, libname=\'ShenZhen\'):\
>     print(\'正在发送邮件\')\
>     from\_addr = \'发件邮箱\'\
>     password = \'发件邮箱密码\'\
> \
>     to\_addr = \'收件邮箱\'\
> \
>     smtp\_server = \'发件邮箱服务器\'\
>     text = dateText + \'A seat is available in \' + libname + \' library on\' + textdate + \'.\'\
>     print(text)\
>     msg = MIMEText(text, \'plain\', \'utf-8\')\
> \
>     msg\[\'From\'\] = Header(from\_addr)\
>     msg\[\'To\'\] = Header(to\_addr)\
>     msg\[\'Subject\'\] = Header(\'Available Seat in \' + libname + \' Library\')\
> \
>     server = smtplib.SMTP\_SSL(host=smtp\_server)\
>     server.quit()\
>     server.connect(smtp\_server, 465)\
>     \# 登录发信邮箱\
>     server.login(from\_addr, password)\
>     \# 发送邮件\
>     server.sendmail(from\_addr, to\_addr, msg.as\_string())\
>     \# 关闭服务器\
>     server.quit()\
>     print(\'邮件成功发送\')

    5. 主程序

        本来是想做一个多进程的程序，同时检测两个图书馆，但是多进程的输入部分会产生未知错误。

> if \_\_name\_\_ == \'\_\_main\_\_\':\
>     toaster.show\_toast(\"Python Script Running\",\
>                        \"Script screening library seat is running\",\
>                        icon\_path=None,\
>                        duration=20,\
>                        threaded=True)\
>     while toaster.notification\_active(): time.sleep(0.1)\
>     username = input(\"请输入读者证号码：\")\
>     password = input(\"请输入密码：\")\
>     print(username)\
>     print(password)\
>     date0 = datetime.datetime.today()\
>     \[mm, dd\] = \[date0.month, date0.day\]\
>     date1 = date0 + datetime.timedelta(days=1)\
>     \[tmm, tdd\] = \[date1.month, date1.day\]\
>     flagdate = int(input(\"Select date:\\n1.today\\n2.tomorrow\\n\"))\
>     if flagdate == 1:\
>         textdate = \"\'\" + str(mm) + \"月\" + str(dd) + \"日\" + \"\'\"\
>     else:\
>         textdate = \"\'\" + str(tmm) + \"月\" + str(tdd) + \"日\" + \"\'\"\
>     listOfLib = \[\[\"ShenZhen\",\
>                   \"https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Factivity\_appt.jsp%3FcategoryId%3D81\"\],\
>                  \[\"FuTian\",\
>                   \"https://www.szlib.org.cn/m/mylibrary/activity\_appt.jsp?categoryId=84&wxKey=cs\_254293649&code=061SWwmi1f6xJr0x8emi1oQbmi1SWwmy&state=1588213084\"\]\]\
>     l1 = Process(target=LibSeatDetect, args=(username, password, textdate, \'ShenZhen\', listOfLib\[0\]\[1\]))\
>     l2 = Process(target=LibSeatDetect, args=(username, password, textdate, \'FuTian\', listOfLib\[1\]\[1\]))\
>     flag = input(\'Choose which library:\\n1.Shenzhen\\n2.FuTian\\nPlease Choose:\')\
>     Processes = \[\]\
>     flag = int(flag)\
>     if flag == 1:\
>         Processes.append(l1)\
>     if flag == 2:\
>         Processes.append(l2)\
>     for l in Processes:\
>         l.start()\
>     for l in Processes:\
>         l.join()\
>     print(\"主程序结束\")

-   **问题**

    1. 进入健康申报界面后的弹窗处理

        健康申报界面提交后会产生弹窗，如不处理，则无法进行下一步。目前采用如下程序切换到弹窗位置处理。

> dialog\_box = drive.switch\_to.alert()\
> print(dialog\_box.text)\
> dialog\_box.accept()

        但是这段程序测试机会少，不了解是否可行，故加上try结构，执行失败后放弃当前窗口，重新开始一次预约流程以跳过健康申报，如下：

> try:\
>     dialog\_box = drive.switch\_to.alert()\
>     print(dialog\_box.text)\
>     dialog\_box.accept()\
> except:\
>     LibSeatDetect(UN, PW, textdate, Libname, webSite)\
>     break

    2. 无重试机制

        程序执行过程中，除等待阶段外网络需要保持链接，如果程序连接失败会报错，无重试机制。

    3.
福田图书馆取分上下午预约，如果两个同时有空位可能会产生未知错误，还未试验过。

-   **操作流程**

    1. 配置好python环境后运行程序

    2. 按照提示，在cmd窗口内逐步选择时间和具体图书馆

    3. 程序自动运行

    4.
检测到空位之后，程序在右下角弹窗（Win10适用），并发送邮件提醒，同时弹出验证码输入框。

    5. 在手机上确认验证码后，输入到验证码输入弹窗内并点击确认

    6. 成功预约，页面在成功预约界面停留10s后自动关闭

-   **预约结果**

![](https://mmbiz.qpic.cn/mmbiz_png/ib3l2I9SSrQmqakwDYDOoZLdG30cV1phK2NayENl4Eh19Jibsib52TLzQkRjTibqvibljDOU5eicG87cxbslGtJSBK4g/640?wx_fmt=png&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1)

-   **GayHub项目地址**（点击原文链接也可以到达）

https://github.com/hantyou/Shenzhen\_Library\_Seat\_Detection
