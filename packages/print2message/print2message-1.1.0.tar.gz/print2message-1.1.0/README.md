## print2message
程序在办公室计算机上运行，想实时了解程序的运行情况或结果？Print2message可以帮你将print内容转发到电子邮件或微信。
### 安装
```bash
pip install print2message
```
### 使用
* 新建yaml配置文件，内容如下：
```
basic:
    subject: 测试用
    method: mail
    switch: true
wechat:
    key: SCU*************
mail:
    host: smtp.qq.com
    port: 25
    password: abcdefg
    user_name: 123456789
    sender: 123456789@qq.com
    receiver: 1234567819@qq.com
```
basic.subject：项目名称，作为消息通知的标题  
basic.method：通知方式，wechat或mail  
basic.swith：是否通知，false将不转发print内容，只单纯执行print功能  
wechat.key：server酱的SCKEY，免费注册  
mail：邮箱的相关参数
* 使用set_config_path指定配置文件位置
### example
```
from print2message import set_config_path, printm
import os

current_path = os.path.dirname(os.path.abspath(__file__))

set_config_path(os.path.join(current_path, 'config.yaml'))

if __name__ == "__main__":
    printm('hello print2msg')
```
