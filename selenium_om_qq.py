import os
import sys
import time,datetime
from multiprocessing import Queue

import win32con
import win32gui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

path_queue = Queue()


class Penguin(object):
    num = 0

    def __init__(self):
        self.url = 'https://om.qq.com/userAuth/index'
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 0.5, 10)

    def login(self):
        self.driver.get(self.url)
        try:
            # 点击选择qq登陆
            self.driver.find_element_by_class_name('login-type-qq').click()
            # 动态iframe的属性用xpath定位到第一个iframe标签，[starts-with(@id, 'qqAuthFrame')]表示开头包含qqAuthFrame
            self.driver.switch_to.frame(self.driver.find_element_by_xpath("//iframe[starts-with(@id, 'qqAuthFrame')]"))
            # 定位到第一个iframe标签后直接根据固定的id定位第二个iframe标签
            self.driver.switch_to.frame('ptlogin_iframe')
            # 等待账号密码的元素加载出来
            self.wait.until(EC.presence_of_element_located((By.ID, 'switcher_plogin')))
            # 点击账号密码登陆
            self.driver.find_element_by_id('switcher_plogin').click()
            time.sleep(1)
            # 通过class属性定位到账号输入框
            self.driver.find_element_by_class_name('inputstyle').send_keys('*********')
            # 通过class中的其中一个唯一的属性定位到密码输入框
            self.driver.find_element_by_class_name('password').send_keys('******')
            # 点击登陆按钮
            self.driver.find_element_by_class_name('login_button').click()
        except:
            pass
        # 循环等待账号登陆成功
        while True:
            try:
                online = self.driver.find_element_by_class_name('link-logout')
                if online:
                    break
            except:
                pass
        time.sleep(0.1)
        self.upload()

    def upload(self):
        # 视频上传页面
        while True:
            self.driver.get('https://om.qq.com/article/articlePublish#/!/view:article?typeName=multivideos')
            # 点击上传新视频按钮
            self.driver.find_element_by_id("btn-upload-video").click()
            # 从队列中取出存放视频文件的路径
            if not path_queue.empty():
                path = path_queue.get()
                # 执行AutoIt脚本
                os.system('upload_video.exe %s' % path)
                self.num += 1
                if self.num >= 40:
                    self.timer(self.upload, day=0, hour=1, min=5, second=0)
                # 提示：	你已在1小时内上传了40个视频，上传过于频繁，请歇一歇再上传
                try:
                    self.driver.find_element_by_class_name('alert-left')
                    self.timer(self.upload, day=0, hour=1, min=5, second=0)
                except:
                    pass
                while True:
                    try:
                        # progress = self.driver.find_element_by_class_name('bar').get_attribute('style')
                        # if progress == 'width: 100%;':
                        #     break

                        # 获取设置封面的src属性，如果src路径存在就跳出循环
                        video_cover = self.driver.find_element_by_class_name('form-video-cover').get_attribute('src')
                        if video_cover:
                            break
                    except:
                        pass
                time.sleep(2)
                self.publish()
            else:
                break

        # Windows弹框
        # dialog = win32gui.FindWindow('#32770', '打开')  # 对话框 chrome
        # ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        #
        # ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        #
        # Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
        #
        # button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button
        #
        # win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, 'E:\\video\\天天这样，谁能顶得住，你是不是心痒痒了？.mp4')  # 往输入框输入绝对地址
        #
        # win32gui.PostMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button

    def publish(self):
        # 点击分类框
        self.driver.find_element_by_class_name('chosen-single').click()
        # 输入分类框下面的输入框按下回车
        self.driver.find_element_by_xpath('//div[@class="chosen-search"]/input').send_keys('电视剧剪辑', Keys.ENTER)
        # 发送标签
        self.driver.find_element_by_xpath('//div[@class="tagsinput"]/div/input').send_keys('电视剧', Keys.ENTER)
        self.driver.find_element_by_xpath('//div[@class="tagsinput"]/div/input').send_keys('爱情', Keys.ENTER)
        self.driver.find_element_by_class_name('inline-block').click()  # 发布按钮
        # 点击发布按钮后页面跳转到发布列表页面，循环等待列表页面出现则发布成功
        while True:
            try:
                finished = self.driver.find_element_by_id('articlelist')
                if finished:
                    break
            except:
                pass

    def file(self):
        for filename in os.listdir('E:\\video'):
            filepath = os.path.join('E:\\video', filename)
            path_queue.put(filepath)

    # 定时循环器
    def timer(self, func, day=0, hour=0, min=0, second=0):
        # 获取当前时间
        now_time = datetime.datetime.now()
        # 当前时间字符串
        str_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
        print('现在时间：',str_time)
        # 时间周期
        period = datetime.timedelta(days=day, hours=hour, minutes=min, seconds=second)
        next_time = now_time + period
        str_next_time = next_time.strftime('%Y-%m-%d %H:%M:%S')
        print("下次执行时间：", str_next_time)
        while True:
            # 获取系统当前时间
            iter_now = datetime.datetime.now()
            iter_now_time = iter_now.strftime('%Y-%m-%d %H:%M:%S')
            if str(iter_now_time) == str(str_next_time):
                func()
                # 获取下一次系统的时间
                iter_time = iter_now + period
                str_next_time = iter_time.strftime('%Y-%m-%d %H:%M:%S')
                # 继续下一次的迭代
                continue


if __name__ == "__main__":
    om = Penguin()
    om.file()
    om.login()






















