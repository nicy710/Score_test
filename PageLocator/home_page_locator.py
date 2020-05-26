from selenium.webdriver.common.by import By


class HomePageLocator:
    # dota2按钮
    DOTA2_button = (By.XPATH, '//i[text()="DOTA2"]')
    # 不同游戏按钮
    game_button = (By.XPATH, '//i[text()="{}"]')
    # 进行中的比赛标题
    process_game_title = (By.XPATH, '//em[text()="进行中的比赛"]')
    # 比赛进行时间
    game_time = (By.XPATH, '//div[@class="si"]//div[@class="two"]')