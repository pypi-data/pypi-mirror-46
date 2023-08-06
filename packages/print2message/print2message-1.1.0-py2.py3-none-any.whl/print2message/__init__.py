'''
@Author: LogicJake
@Date: 2019-05-24 19:36:35
@LastEditTime: 2019-05-24 20:10:25
'''
import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText

import requests
import yaml

config = {'config_path': ''}


def set_config_path(path):
    config['config_path'] = path


class SendMessage:
    def __init__(self):
        self.content = ""

    def flush(self):
        pass

    def write(self, s):
        self.content += s

    def send_msg(self):
        f = open(config['config_path'], 'r', encoding='utf-8')
        d = yaml.load(f, Loader=yaml.SafeLoader)
        f.close()

        try:
            is_open = d['basic']['switch']

            if is_open:
                method = d['basic']['method']
                subject = d['basic']['subject']

                if method == 'wechat':
                    key = d['wechat']['key']

                    data = {'text': subject, 'desp': self.content}
                    url = 'https://sc.ftqq.com/{}.send'.format(key)
                    r = requests.post(url, data=data)

                    res = json.loads(r.text)
                    if res['errno'] != 0:
                        raise Exception(res['errmsg'])
                elif method == 'mail':
                    host = d['mail']['host']
                    port = d['mail']['port']
                    password = d['mail']['password']
                    user_name = d['mail']['user_name']
                    sender = d['mail']['sender']
                    receiver = d['mail']['receiver']

                    message = MIMEText(self.content, 'plain', 'utf-8')
                    message['From'] = Header("{}通知".format(subject), 'utf-8')
                    message['To'] = Header(receiver, 'utf-8')
                    message['Subject'] = Header(subject, 'utf-8')

                    smtpObj = smtplib.SMTP()
                    smtpObj.connect(host, port)
                    smtpObj.login(user_name, password)
                    smtpObj.sendmail(sender, receiver, message.as_string())

        except Exception as e:
            print('print2msg error:', e)


def printm(*args, sep=' ', end='\n', file=None, flush=False):
    f = SendMessage()
    print(*args, sep=sep, end=end, file=f)
    f.send_msg()

    # 正常输出
    print(*args, sep=sep, end=end, file=file, flush=flush)
