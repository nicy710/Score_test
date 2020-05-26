from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common import read_path
# from Common import logger
import logging
import time
# import win32gui
# import win32con


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_ele_visible(self, locator, wait_time=20, poll_frequency=0.5, model_name=''):
        """
        等待元素可见
        :param locator:类型为元组（By.XXX, 定位表达式）
        :param wait_time:等待时间
        :param poll_frequency:等待间隔时间
        :param model_name:模块名
        :return:
        """
        try:
            # 开始时间
            start_time = time.time()
            WebDriverWait(self.driver, wait_time, poll_frequency).until(EC.visibility_of_element_located(locator))
            end_time = time.time()
            run_time = end_time - start_time
            logging.info('起始时间是{0}，结束时间是{1}，运行时间是{2}'.format(start_time, end_time, run_time))
        except:
            # 捕获异常到日志中
            logging.exception('等待元素可见失败：')
            # 截图 -- 保存到指定的目录
            self._screenshoot(model_name)
            # 抛出异常
            raise

    def get_element(self, locator, model_name=''):
        """
        查找元素（单个）
        :param locator: 类型为元组（By.XXX, 定位表达式）
        :return: 返回元素
        """
        try:
            return self.driver.find_element(*locator)
        except:
            # 捕获异常到日志中
            logging.exception('定位元素失败：')
            # 截图 -- 保存到指定的目录
            self._screenshoot(model_name)
            # 抛出异常
            raise

    def get_elements(self, locator, model_name=''):
        """
        查找元素（多个）
        :param locator: 类型为元组（By.XXX, 定位表达式）
        :return: 返回元素
        """
        try:
            return self.driver.find_elements(*locator)
        except:
            # 捕获异常到日志中
            logging.exception('定位元素失败：')
            # 截图 -- 保存到指定的目录
            self._screenshoot(model_name)
            # 抛出异常
            raise

    def input_text(self, locator, text, model_name=''):
        """
        输入操作
        :param locator:类型为元组（By.XXX, 定位表达式）
        :param text:输入的内容
        :return:
        """
        # 找到元素
        element = self.get_element(locator)
        # 输入内容
        try:
            element.send_keys(text)
        except:
            # 捕获异常到日志中
            logging.exception('输入失败：')
            # 截图 -- 保存到指定的目录
            self._screenshoot(model_name)
            # 抛出异常
            raise

    def click_element(self, locator, model_name=''):
        """
        点击操作
        :param locator: 类型为元组（By.XXX, 定位表达式）
        :return:
        """
        # 找到元素
        element = self.get_element(locator)
        # 输入内容
        try:
            element.click()
        except:
            # 捕获异常到日志中
            logging.exception('点击元素失败：')
            # 截图 -- 保存到指定的目录
            self._screenshoot(model_name)
            # 抛出异常
            raise

    def get_element_attribute(self, locator, attr_name, model_name=''):
        """
        获取元素属性
        :param locator: 类型为元组（By.XXX, 定位表达式）
        :param attr_name: 属性名
        :return: 属性值
        """
        # 找到元素
        element = self.get_element(locator)
        # 获取属性值
        try:
            return element.get_attribute(attr_name)
        except:
            # 捕获异常到日志中
            logging.exception('获取元素属性值失败：')
            # 截图 -- 保存到指定的目录
            self._screenshoot(model_name)
            # 抛出异常
            raise

    def get_element_text(self, locator, model_name=''):
        """
        获取元素文本
        :param locator: 类型为元组（By.XXX, 定位表达式）
        :param model_name: 模块名
        :return: 元素文本
        """
        # 找到元素
        element = self.get_element(locator)
        # 获取元素文本
        try:
            return element.text
        except:
            # 捕获异常到日志中
            logging.exception('获取元素文本失败：')
            # 截图 -- 保存到指定的目录
            self._screenshoot(model_name)
            # 抛出异常
            raise

    def _screenshoot(self, model_name):
        """截屏"""
        file_path = read_path.screenshoot_path + '/{0}_{1}.png'.format(model_name, time.strftime('%Y%m%d_%H%M%S'))
        self.driver.save_screenshot(file_path)
        logging.info('保存截图成功，路径为：{0}'.format(file_path))

    # def upload_chrome(self, file_path, model_name=''):
    #     """谷歌浏览器上传文件"""
    #     # 一级窗口
    #     dialog = win32gui.FindWindow('#32770', '打开')
    #     # 二级窗口
    #     ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
    #     # 三级窗口
    #     comboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
    #     # 四级窗口 - 文件路径输入框
    #     edit = win32gui.FindWindowEx(comboBox, 0, 'Edit', None)
    #     # 二级窗口 - 打开按钮
    #     button = win32gui.FindWindowEx(dialog, 0, 'Button', '打开(&O)')
    #     try:
    #         # 操作 - 发送文件路径
    #         win32gui.SendMessage(edit, win32con.WM_SETTEXT, None, file_path)
    #         # 点击打开按钮
    #         win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)
    #     except:
    #         # 捕获异常到日志中
    #         logging.exception('文件上传失败：')
    #         # 截图 -- 保存到指定的目录
    #         self._screenshoot(model_name)
    #         # 抛出异常
    #         raise
