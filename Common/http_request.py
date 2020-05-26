import requests
import logging
from Common import logger


class HttpRequest:
    def http_request(self, url, request_data, method, cookies):

        if method.lower() == 'get':
            try:
                res = requests.get(url, request_data, cookies=cookies)
            except Exception as e:
                logging.error('get请求出错了，错误是：{0}'.format(e))
                raise e
        elif method.lower() == 'post':
            try:
                res = requests.post(url, request_data, cookies=cookies)
            except Exception as e:
                logging.error('post请求出错了，错误是：{0}'.format(e))
                raise e
        else:
            return '参数方式错误'
        return res
