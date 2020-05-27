from selenium import webdriver
from Common.send_alarm import SendAlarm

driver = webdriver.Firefox()
driver.get('https://www.baidu.com/')
SendAlarm().send_dingtalk_alarm('打开浏览器了')
driver.close()