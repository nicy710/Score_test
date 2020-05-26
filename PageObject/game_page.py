from Common.base_page import BasePage
from PageLocator.game_page_locator import GamePageLocator
from Common.send_alarm import SendAlarm
import time
from Common import logger
import logging


class GamePage(BasePage, GamePageLocator):

    def judge_score_detail(self):
        """判断赛况详情是否存在，没有则刷新页面，刷新10次仍没有数据返回false，有数据返回true"""
        name = '判断赛况详情是否存在'
        score_detail_element = self.get_elements(self.score_detail_block, model_name=name)
        retry_count = 0
        while not score_detail_element and retry_count < 10:
            # 如果赛况数据为空，刷新页面
            self.driver.refresh()
            time.sleep(3)
            score_detail_element = self.get_elements(self.score_detail_block, model_name=name)
            retry_count += 1
        if retry_count >= 10 and not score_detail_element:
            url = self.driver.current_url
            logging.error('-------------获取赛况数据失败------------')
            SendAlarm().send_dingtalk_alarm('获取赛况数据失败，地址是：{}'.format(url))
            self.driver.quit()
            return False
        if score_detail_element:
            return True

    def get_score_data(self):
        """获取比分数据"""
        name = '获取比分数据'
        self.wait_ele_visible(self.score_data_text, model_name=name)
        score_data = self.get_element_text(self.score_data_text, model_name=name).split()
        return score_data

    def compare_data(self):
        """
        对比数据，每10S获取一次数据与上次做对比，如果数据不同则继续获取数据对比，
        如果数据相同则继续对比，5分钟后仍相同则刷新页面
        """
        score_data_0 = self.get_score_data()
        time.sleep(10)
        score_data_1 = self.get_score_data()

        while True:
            compare_count = 0
            # 如果数据不同则继续获取数据进行对比
            while score_data_0 != score_data_1:
                score_data_0 = score_data_1
                time.sleep(10)
                score_data_1 = self.get_score_data()

            # 如果数据相同且对比次数少于30次，则继续获取数据进行对比
            while score_data_0 == score_data_1 and compare_count < 30:
                score_data_0 = score_data_1
                time.sleep(10)
                score_data_1 = self.get_score_data()
                compare_count += 1
                logging.info('----------第{}次数据对比没有变化----------'.format(compare_count))

            # 数据相同次数大于等于30次，停止对比数据，刷新页面
            if compare_count >= 30:
                self.driver.refresh()
                logging.info('----------5分钟后数据没有变化----------')
                break

    def judge_game_finish(self):
        """
        判断游戏是否结束，通过判断是否有胜败方图标来返回
        如果有图标，表示游戏结束，返回True
        如果没有图标，表示游戏未结束，返回False
        """
        name = '判断游戏是否结束'
        # shengbai_left_img_element = self.get_element(self.shengbai_left_img, model_name=name)
        style_attr = self.get_element_attribute(self.shengbai_left_img, 'style', model_name=name)
        # print(style_attr)
        if style_attr == 'display: none;':
            logging.info('----------当前小局比赛未结束----------')
            return False
        else:
            logging.info('----------当前小局比赛已结束----------')
            return True

    def judge_data_change(self):
        """判断数据是否实时变化,如果有变化返回True，如果不变返回False"""
        score_data_0 = self.get_score_data()
        time.sleep(10)
        score_data_1 = self.get_score_data()
        if score_data_0 != score_data_1:
            logging.info('----------数据有实时变化----------')
            return True
        else:
            logging.info('----------数据没有实时变化----------')
            return False


if __name__ == '__main__':
    from selenium import webdriver
    # import time
    driver = webdriver.Chrome()
    driver.get('https://dawnbytes.com/detail?id=77822774013740160')
    time.sleep(3)
    a = GamePage(driver).judge_game_finish()
    print(a)