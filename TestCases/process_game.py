from selenium import webdriver
from PageObject.home_page import HomePage
from PageObject.game_page import GamePage
from TestData import common_data
from Common.send_alarm import SendAlarm
from Common.read_config import ReadConfig
from Common import read_path
from Common import logger
import logging
import time


class Score:
    @staticmethod
    def process_game(game_button):
        while eval(ReadConfig().read_config(read_path.conf_path, 'BASE', 'run_flg')):
            driver = webdriver.Chrome()
            # driver.maximize_window()
            driver.get(common_data.test_url)
            home_page = HomePage(driver)

            # 点击游戏DOTA2
            logging.info('----------开始点击DOTA2游戏按钮----------')
            # home_page.judge_dota2_button().click_dota2_button()
            home_page.judge_game_button(game_button).click_game_button(game_button)
            time.sleep(3)
            # home_page.click_dota2_button()
            home_page.click_game_button(game_button)
            logging.info('----------点击成功！----------')

            # 判断是否有进行中的游戏，如果有则进入游戏，没有则5分钟获取一次数据，直到有数据为止
            logging.info('----------开始进入进行中游戏----------')
            time.sleep(5)
            home_page.judge_process_game()[0].click()

            # 切换窗口
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])

            # 判断是否有赛况数据，有数据则进入数据对比，没有数据则抛出异常
            game_page = GamePage(driver)
            if game_page.judge_score_detail():
                # 先判断比赛是否结束
                logging.info('----------比赛状态为{}----------'.format(game_page.judge_game_finish()))
                if not game_page.judge_game_finish():
                    # 如果没有胜败图标表示比赛进行中
                    logging.info('----------开始进行数据对比----------')
                    data_change_flg = True
                    while data_change_flg:
                        game_page.compare_data()
                        # 对比完成刷新页面后，判断能否正常获取赛况数据
                        if game_page.judge_score_detail():
                            # 如果能正常获取赛况数据，判断能否有胜败方图标（比赛是否结束）
                            if game_page.judge_game_finish():
                                # 如果有胜败方图标，说明比赛结束，退出浏览器
                                data_change_flg = False
                                driver.quit()
                            else:
                                # 如果没有胜败方图标，说明比赛未结束，继续判断数据是否实时变化
                                if game_page.judge_data_change():
                                    # 如果数据有实时变化，则继续对比数据
                                    logging.info('----------websocket数据推送断掉，刷新后已重新推送数据----------')
                                    continue
                                else:
                                    # 如果数据没有实时变化，说明数据推送有问题，抛出异常
                                    url = driver.current_url
                                    logging.info('----------数据推送异常，无法实时更新数据！！！----------')
                                    SendAlarm().send_dingtalk_alarm('数据推送异常，无法实时更新数据，地址是：{}'.format(url))
                                    driver.quit()
                        else:
                            # 如果不能获取赛况数据，抛出异常，跳出循环
                            data_change_flg = False
                else:
                    # 如果有胜败图标，表示比赛已结束
                    driver.quit()
                    logging.info('----------比赛怎么结束了？？？----------')


if __name__ == '__main__':

    try:
        Score().process_game('DOTA2')
    except Exception as e:
        SendAlarm().send_dingtalk_alarm('程序异常停止：{}'.format(e))
        raise e