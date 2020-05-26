import time
from Common.base_page import BasePage
from PageLocator.home_page_locator import HomePageLocator
from TestData import common_data
from Common import logger
import logging


class HomePage(HomePageLocator, BasePage):

    def click_dota2_button(self):
        """点击DOTA2按钮"""
        name = '击DOTA2按钮'
        self.wait_ele_visible(self.DOTA2_button, model_name=name)
        self.click_element(self.DOTA2_button, model_name=name)
        return self

    def click_game_button(self, game_name):
        """点击游戏按钮"""
        name = '点击DOTA2按钮'
        self.wait_ele_visible((self.game_button[0], self.game_button[1].format(game_name)), model_name=name)
        self.click_element((self.game_button[0], self.game_button[1].format(game_name)), model_name=name)
        return self

    def judge_dota2_button(self):
        """判断DOTA2按钮是否存在，存在则继续，不存在重新访问页面"""
        name = '判断DOTA2按钮是否存在'
        button_element = self.get_elements(self.DOTA2_button, model_name=name)
        while not button_element:
            self.driver.get(common_data.test_url)
            button_element = self.get_elements(self.DOTA2_button, model_name=name)
        return self

    def judge_game_button(self, game_name):
        """判断对应游戏按钮是否存在，存在则继续，不存在重新访问页面"""
        name = '判断对应游戏按钮是否存在'
        button_element = self.get_elements((self.game_button[0], self.game_button[1].format(game_name)), model_name=name)
        while not button_element:
            self.driver.get(common_data.test_url)
            button_element = self.get_elements((self.game_button[0], self.game_button[1].format(game_name)),
                                               model_name=name)
        return self

    def get_process_game(self):
        """获取进行中比赛"""
        name = '获取进行中比赛'
        process_game_list = []
        if len(self.get_elements(self.process_game_title, name)) > 0:
            if len(self.get_elements(self.game_time, name)) > 0:
                for i in self.get_elements(self.game_time, name):
                    if i.text != '0:00':
                        process_game_list.append(i)
        return process_game_list

    def judge_process_game(self):
        """判断是否有进行中比赛，有则返回进行中的比赛，没有则每5分钟获取一次数据，直到有比赛"""
        process_game = self.get_process_game()
        retry_count = 0
        while not process_game:
            time.sleep(10)
            self.click_dota2_button()
            retry_count += 1
            logging.info('----------点击了{}次DOTA2按钮----------'.format(retry_count))
            time.sleep(3)
            process_game = self.get_process_game()
        logging.info('----------进行中的比赛有{}场----------'.format(len(process_game)))
        return process_game
