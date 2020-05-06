# coding=utf-8
from selenium import webdriver
import time
import winsound
import tkinter as tk
from tkinter import messagebox
import datetime
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header

from win10toast import ToastNotifier
from multiprocessing import Process

toaster = ToastNotifier()
# 用于构建邮件头
VarValue = ''


def sendAnEmail(dateText, textdate, libname='ShenZhen'):
    print('正在发送邮件')
    from_addr = ''
    password = ''
    to_addr = ''
    smtp_server = ''

    text = dateText + 'A seat is available in ' + libname + ' library on' + textdate + '.'
    print(text)
    msg = MIMEText(text, 'plain', 'utf-8')

    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('Available Seat in ' + libname + ' Library')

    server = smtplib.SMTP_SSL(host=smtp_server)
    server.quit()
    server.connect(smtp_server, 465)
    # 登录发信邮箱
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, to_addr, msg.as_string())
    # 关闭服务器
    server.quit()
    print('邮件成功发送')


class MyCollectApp(tk.Toplevel):  # 重点
    def __init__(self):
        super().__init__()  # 重点
        self.setupUI()
        self.title('验证码')

    def setupUI(self):
        row1 = tk.Frame(self)
        row1.pack(fill="x")
        l1 = tk.Label(row1, text="验证码：", height=2, width=10)
        l1.pack(side=tk.LEFT)  # 这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
        self.xls_text = tk.StringVar()
        tk.Entry(row1, textvariable=self.xls_text).pack(side=tk.RIGHT)

        row2 = tk.Frame(self)
        row2.pack(fill="x")
        tk.Button(row2, text="点击确认", command=self.on_click).pack(side=tk.RIGHT)

    def on_click(self):
        # print(self.xls_text.get().lstrip())
        global VarValue
        VarValue = self.xls_text.get().lstrip()
        if len(VarValue) == 0:
            # print("用户名必须输入!")
            messagebox.showwarning(title='系统提示', message='请输入验证码!')
            return False

        self.quit()
        self.destroy()


def LibSeatDetect(UN, PW, textdate, Libname="ShenZhen",
                  webSite="https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Factivity_appt.jsp%3FcategoryId%3D81"):
    # 配置文件地址
    print(Libname + "图书馆的位置检测已经开始")
    global VarValue
    toaster.show_toast("LibDectec Running of " + Libname + "Library",
                       "Script screening library seat of " + Libname + " library is running",
                       icon_path=None,
                       duration=20,
                       threaded=True)
    while toaster.notification_active(): time.sleep(0.1)
    profile_directory = r'C:\Users\Daniel Zhai\AppData\Roaming\Mozilla\Firefox\Profiles\sgjgzcra.default'
    # 加载配置配置
    profile = webdriver.FirefoxProfile(profile_directory)
    # 启动浏览器配置
    drive = webdriver.Firefox(profile)

    # drive = webdriver.Firefox()
    drive.get(webSite)
    # drive.get("http://www.szlib.org.cn")
    # drive.get("http://www.baidu.com")
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

    while 1:
        failCount += 1
        """检测当前监控的位置是否可以预约"""
        if not drive.find_element_by_xpath(
                "//span[contains(text()," + textdate + ")]/following-sibling::a").text == u"去预约" in drive.page_source:
            pass
        else:
            print('\033[32m有空位[30m')
            date = datetime.datetime.now()
            dateText = str(date.year) + r'-' + str(date.month) + r'-' + str(date.day) + r'-' + str(
                date.hour) + ':' + str(
                date.minute) + ':' + str(date.second)
            print(dateText)
            """进入预约界面"""
            yuyue = drive.find_element_by_css_selector("[class='comment_score gotoyy']")
            drive.execute_script("arguments[0].scrollIntoView();", yuyue)
            yuyue.click()
            """检测是否需要填写健康信息"""
            if u"请填写您的健康信息" in drive.page_source:
                drive.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[2]/form/div/div/div/div/div[1]/div[2]/input[2]").click()
                time.sleep(1)
                drive.find_element_by_xpath(
                    "/html/body/div[1]/div[2]/div[2]/form/div/div/div/div/div[2]/div[2]/input[2]").click()
                known = drive.find_element_by_xpath("//*[@id='c1']")
                if not known.is_selected():
                    known.click()
                drive.find_element_by_class_name("page_btn").click()
            """进入预约信息填写界面"""
            drive.find_element_by_id("getCheckCode").click()
            """在预约前发送邮件通知"""
            if not SentEmail:
                try:
                    sendAnEmail(dateText, textdate, Libname)
                except:
                    print("发送邮件失败，跳过")
                    pass
            """跳出验证码填写界面"""
            app = MyCollectApp()
            app.mainloop()
            print(VarValue)
            """请求验证码"""
            drive.find_element_by_css_selector("[class='input w_small required']").click()
            drive.find_element_by_css_selector("[name='applyCheckCode']").send_keys(VarValue)
            drive.find_element_by_css_selector("[class='submit btn_2']").click()
            break
        """隔一段时间再刷新"""
        if failCount < 10:
            for i in range(1, 6):
                time.sleep(1)
                last_time = 6 - i
                print('\rNo Seat in ' + Libname + ' library, temporarily stop detection for %s seconds.' % last_time,
                      end="")

        else:
            for i in range(1, 121):
                time.sleep(1)
                last_time = 121 - i
                print(
                    '\rNo Seat in ' + Libname + ' library for a long time, temporarily stop detection for %s seconds.' % last_time,
                    end="")
            failCount = 0
        drive.refresh()
    time.sleep(1)
    drive.quit()
    quit()


if __name__ == '__main__':
    VarValue = ''
    toaster.show_toast("Python Script Running",
                       "Script screening library seat is running",
                       icon_path=None,
                       duration=20,
                       threaded=True)
    while toaster.notification_active(): time.sleep(0.1)
    username = input("请输入读者证号码：")
    password = input("请输入密码：")
    print(username)
    print(password)
    date0 = datetime.datetime.today()
    [mm, dd] = [date0.month, date0.day]
    date1 = date0 + datetime.timedelta(days=1)
    [tmm, tdd] = [date1.month, date1.day]
    flagdate = int(input("Select date:\n1.today\n2.tomorrow\n"))
    if flagdate == 1:
        textdate = "'" + str(mm) + "月" + str(mm) + "日" + "'"
    else:
        textdate = "'" + str(tmm) + "月" + str(tdd) + "日" + "'"
    listOfLib = [["ShenZhen",
                  "https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Factivity_appt.jsp%3FcategoryId%3D81"],
                 ["FuTian",
                  "https://www.szlib.org.cn/m/mylibrary/activity_appt.jsp?categoryId=84&wxKey=cs_254293649&code=061SWwmi1f6xJr0x8emi1oQbmi1SWwmy&state=1588213084"]]
    l1 = Process(target=LibSeatDetect, args=(username, password, textdate, 'ShenZhen', listOfLib[0][1]))
    l2 = Process(target=LibSeatDetect, args=(username, password, textdate, 'FuTian', listOfLib[1][1]))
    flag = input('Choose which library:\n1.Shenzhen\n2.FuTian\nPlease Choose:')
    Processes = []
    flag = int(flag)
    # Processes.append(l1)
    if flag == 1:
        Processes.append(l1)
    if flag == 2:
        Processes.append(l2)
    for l in Processes:
        l.start()
    for l in Processes:
        l.join()

    print("主程序结束")
