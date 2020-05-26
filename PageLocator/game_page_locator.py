from selenium.webdriver.common.by import By


class GamePageLocator:
    # 赛况详情
    score_detail_block = (By.XPATH, '//div[@class="score-detail"]')
    # 比分数据
    score_data_text = (By.XPATH, '//div[@class="img-list"]')
    # 左边胜败方图标
    shengbai_left_img = (By.XPATH, '//div[@class="shengbai-left"]')