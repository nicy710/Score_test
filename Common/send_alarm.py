import datetime
import requests
from Common import read_path
from Common.read_config import ReadConfig


class SendAlarm:
    def send_alarm_text(self, msg):
        """向文本文件添加报警信息"""
        alarm_time = datetime.datetime.now().strftime('%Y-%m-%d %T')
        with open(read_path.alarm_path, 'a', encoding='utf-8') as file:
            file.write(alarm_time + '  ' + msg + '\n')
        print(alarm_time)

    def send_dingtalk_alarm(self, msg):
        """向钉钉发送警报"""
        url = ReadConfig().read_config(read_path.conf_path, 'BASE', 'dingtalk_alarm_url')
        data = '{"msgtype": "text","text": {"content": "监控报警：' + msg + '"}}'
        header = {'Content-Type': 'application/json'}
        requests.post(url, json=eval(data), headers=header)


if __name__ == '__main__':
    # SendAlarm().send_alarm_text('测试报警！！！')
    SendAlarm().send_dingtalk_alarm('测试报警！！！')