from TestCases.process_game import Score
from Common.send_alarm import SendAlarm

try:
    Score().process_game('DOTA2')
except Exception as e:
    SendAlarm().send_dingtalk_alarm('程序异常停止：{}'.format(e))
    raise e