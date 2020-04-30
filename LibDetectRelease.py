# coding=utf-8
from selenium import webdriver
import time
from tkinter import messagebox
import datetime
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
from win10toast import ToastNotifier
from multiprocessing import Process
toaster = ToastNotifier()
"""需要手动添加的库有 selenium, win10toast"""
# 无icon，采用python的icon，且采用自己的线程
toaster.show_toast("Python Script Running",
                   "Script screening library seat is running",
                   icon_path=None,
                   duration=20,
                   threaded=True)
while toaster.notification_active(): time.sleep(0.1)


# 用于构建邮件头


def sendAnEmail(dateText, libname='ShenZhen'):
    print('正在发送邮件')

    from_addr = ''  # 发件人地址
    password = ''  # 发件人邮箱密码
    to_addr = ''  # 收件人地址

    smtp_server = ''
    text = dateText + 'A seat is available in ' + libname + 'library.'
    print(text)
    msg = MIMEText(text, 'plain', 'utf-8')

    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('Available Seat in ' + libname + ' Library')

    server = smtplib.SMTP_SSL()
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    print('邮件成功发送')


def LibSeatDetect(UN, PW, Libname="ShenZhen",
                  webSite="https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Factivity_appt.jsp%3FcategoryId%3D81"):
    # 配置文件地址
    print(Libname + "图书馆的位置检测已经开始")

    toaster.show_toast("LibDectec Running of " + Libname + "Library",
                       "Script screening library seat of " + Libname + " library is running",
                       icon_path=None,
                       duration=20,
                       threaded=True)
    while toaster.notification_active(): time.sleep(0.1)

    """把下面这一行改成自己的浏览器配置地址"""
    profile_directory = r'C:\Users\Daniel Zhai\AppData\Roaming\Mozilla\Firefox\Profiles\sgjgzcra.default'
    # 加载配置配置
    profile = webdriver.FirefoxProfile(profile_directory)
    # 启动浏览器配置
    drive = webdriver.Firefox(profile)
    drive.get(webSite)
    aa = drive.get_cookies()
    print(aa)
    print(11)
    url = drive.current_window_handle
    drive.switch_to.window(url)
    name = UN
    password = PW
    print("正在登陆" + Libname + "图书馆，账号：" + name + "\n密码：" + password)
    drive.find_element_by_name("username").clear()
    drive.find_element_by_name("username").send_keys(name)
    drive.find_element_by_name("password").clear()
    drive.find_element_by_name("password").send_keys(password)
    drive.find_element_by_class_name("submit").click()
    SentEmail = False
    failCount = 0
    while (1):
        failCount += 1
        print('现在' + Libname + '图书馆有预约名额吗？')
        print(u"去预约" in drive.page_source)
        if u"去预约" in drive.page_source:
            failCount = 0
            messagebox.showinfo("提示", Libname + "图书馆可以预约啦")
            date = datetime.datetime.now()
            dateText = str(date.year) + r'-' + str(date.month) + r'-' + str(date.day) + r'-' + str(
                date.hour) + ':' + str(
                date.minute) + ':' + str(date.second)
            print(dateText)
            if not SentEmail:
                toaster.show_toast("A Library Seat in " + Libname + " Library!",
                                   "A new library seat is available",
                                   icon_path=None,
                                   duration=10,
                                   threaded=True)
                while toaster.notification_active(): time.sleep(0.1)
                SentEmail = True
                """如果需要发送邮件，自行配置下列函数中的参数"""
                # sendAnEmail(dateText, Libname)
        if failCount < 10:
            time.sleep(5)
            print('No Seat in ' + Libname + ' library, temporarily stop detection for 5 seconds.')
        else:
            print(
                'No Seat in ' + Libname + ' library for a long time (5 seconds, 10 times), temporarily stop detection for 2 minute.')
            time.sleep(120)
            failCount = 0
        drive.refresh()
    time.sleep(1)
    drive.quit()


username = input("请输入读者证号码：")
password = input("请输入密码：")

listOfLib = [["ShenZhen",
              "https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Factivity_appt.jsp%3FcategoryId%3D81"],
             ["FuTian",
              "https://www.szlib.org.cn/m/mylibrary/activity_appt.jsp?categoryId=84&wxKey=cs_254293649&code=061SWwmi1f6xJr0x8emi1oQbmi1SWwmy&state=1588213084"]]
l1 = Process(target=LibSeatDetect, args=(username, password, 'ShenZhen', listOfLib[0][1]))
l2 = Process(target=LibSeatDetect, args=(username, password, 'FuTian', listOfLib[1][1]))
Processes = []

Processes.append(l1)
Processes.append(l2)
if __name__ == '__main__':
    for l in Processes:
        l.start()
    for l in Processes:
        l.join()

    print("主程序结束")
