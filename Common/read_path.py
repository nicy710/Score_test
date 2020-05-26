import os

# 项目文件路径
pro_path = os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

# 测试log路径
log_path = os.path.join(pro_path, 'logs', 'test_log.txt')

# 报警文件
alarm_path = os.path.join(pro_path, 'logs', 'alarm.txt')

# 截屏文件路径
screenshoot_path = os.path.join(pro_path, 'ScreenShoot')

# 配置文件路径
conf_path = os.path.join(pro_path, 'conf', 'base.conf')
